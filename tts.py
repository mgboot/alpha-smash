"""Azure Text-to-Speech integration for Alpha Smash.

Speaks completed words aloud using Azure Cognitive Services.
Requires ``az login`` and a valid SPEECH_ENDPOINT in config.py.
Gracefully degrades to silence when Azure is unavailable.
"""

import logging
import os
import threading

log = logging.getLogger(__name__)

_speech_config = None
_audio_config = None
_initialized = False
_available = False

_speaking = False
_lock = threading.Lock()


def _init():
    """Lazy-initialise Azure Speech SDK and credentials."""
    global _speech_config, _audio_config, _initialized, _available
    if _initialized:
        return
    _initialized = True

    endpoint = os.environ.get("SPEECH_ENDPOINT", "").strip()
    if not endpoint:
        log.info("TTS disabled — SPEECH_ENDPOINT not set in .env")
        return

    try:
        from azure.identity import AzureCliCredential
        import azure.cognitiveservices.speech as speechsdk

        credential = AzureCliCredential()
        token = credential.get_token(
            "https://cognitiveservices.azure.com/.default"
        ).token
        _speech_config = speechsdk.SpeechConfig(endpoint=endpoint)
        _speech_config.authorization_token = token
        _audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        _available = True
        log.info("Azure TTS initialised")
    except Exception as exc:
        log.warning("Azure TTS unavailable: %s", exc)
        _available = False


def _build_spelling_ssml(word, voice, lang):
    """Build SSML that spells out each letter with explicit IPA phonemes."""
    from words import LETTER_PHONEMES

    # Derive xml:lang from voice name (e.g. "en-US" from "en-US-AvaNeural")
    parts = voice.split("-")
    xml_lang = f"{parts[0]}-{parts[1]}"

    phonemes = LETTER_PHONEMES.get(lang, {})
    ipa_parts = [phonemes.get(char) for char in word]

    # Single <phoneme> with IPA syllable-boundary dots so the engine
    # pauses between letters without the choppy start/stop of separate
    # elements.
    if all(ipa_parts):
        body = (
            f'<phoneme alphabet="ipa" ph="{".".join(ipa_parts)}">'
            f'{word}</phoneme>'
        )
    else:
        # Fallback: mix phoneme-tagged and plain characters
        elements = []
        for char, ph in zip(word, ipa_parts):
            if ph:
                elements.append(
                    f'<phoneme alphabet="ipa" ph="{ph}">{char}</phoneme>'
                )
            else:
                elements.append(char)
        body = '<break time="350ms"/>'.join(elements)

    return (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{xml_lang}">'
        f'<voice name="{voice}">{body}</voice>'
        '</speak>'
    )


def speak_celebration(word, lang, phrase, article=None):
    """Speak the celebration sequence asynchronously: spell → word → phrase.

    When *article* is provided (e.g. "das" for German), TTS speaks
    ``"article word"`` instead of just ``word`` to reinforce grammatical gender.
    """
    global _speaking
    _init()
    if not _available:
        return

    from config import TTS_VOICES
    import azure.cognitiveservices.speech as speechsdk

    voice = TTS_VOICES.get(lang)
    if not voice:
        return

    # Build SSML for spelling out each letter with correct pronunciation
    ssml = _build_spelling_ssml(word, voice, lang)

    # Lowercase the word so TTS doesn't treat it as an acronym.
    # German nouns keep an initial capital (e.g. "Katze").
    spoken_word = word.capitalize() if lang == "de" else word.lower()
    if article:
        spoken_word = f"{article} {spoken_word}"

    with _lock:
        _speaking = True

    def _run():
        global _speaking
        try:
            _speech_config.speech_synthesis_voice_name = voice

            # Step 1: Spell out letters using SSML phonemes
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=_speech_config,
                audio_config=_audio_config,
            )
            result = synthesizer.speak_ssml_async(ssml).get()
            if result.reason == speechsdk.ResultReason.Canceled:
                details = result.cancellation_details
                log.warning("TTS canceled: %s %s", details.reason,
                            details.error_details or "")
            else:
                # Steps 2-3: Speak word (with article) and celebration phrase
                for text in (spoken_word, phrase):
                    synthesizer = speechsdk.SpeechSynthesizer(
                        speech_config=_speech_config,
                        audio_config=_audio_config,
                    )
                    result = synthesizer.speak_text_async(text).get()
                    if result.reason == speechsdk.ResultReason.Canceled:
                        details = result.cancellation_details
                        log.warning("TTS canceled: %s %s", details.reason,
                                    details.error_details or "")
                        break
        except Exception as exc:
            log.warning("TTS playback failed: %s", exc)
        finally:
            with _lock:
                _speaking = False

    threading.Thread(target=_run, daemon=True).start()


def speak_language_name(lang):
    """Speak the language name (e.g. 'Deutsch') in its own voice. Non-blocking."""
    global _speaking
    _init()
    if not _available:
        return

    from config import TTS_VOICES
    import azure.cognitiveservices.speech as speechsdk

    voice = TTS_VOICES.get(lang)
    if not voice:
        return

    names = {"en": "English", "es": "Español", "de": "Deutsch"}
    text = names.get(lang, "")
    if not text:
        return

    with _lock:
        _speaking = True

    def _run():
        global _speaking
        try:
            _speech_config.speech_synthesis_voice_name = voice
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=_speech_config,
                audio_config=_audio_config,
            )
            result = synthesizer.speak_text_async(text).get()
            if result.reason == speechsdk.ResultReason.Canceled:
                details = result.cancellation_details
                log.warning("TTS canceled: %s %s", details.reason,
                            details.error_details or "")
        except Exception as exc:
            log.warning("TTS playback failed: %s", exc)
        finally:
            with _lock:
                _speaking = False

    threading.Thread(target=_run, daemon=True).start()


def is_speaking():
    """Return True while TTS audio is still playing."""
    with _lock:
        return _speaking
