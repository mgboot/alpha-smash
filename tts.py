"""Azure Text-to-Speech integration for Alpha Smash.

Speaks completed words aloud using Azure Cognitive Services.
Requires ``az login`` and a valid SPEECH_ENDPOINT in config.py.
Gracefully degrades to silence when Azure is unavailable.
"""

import logging
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

    from config import SPEECH_ENDPOINT
    if not SPEECH_ENDPOINT:
        log.info("TTS disabled — SPEECH_ENDPOINT not set in config.py")
        return

    try:
        from azure.identity import AzureCliCredential
        import azure.cognitiveservices.speech as speechsdk

        credential = AzureCliCredential()
        token = credential.get_token(
            "https://cognitiveservices.azure.com/.default"
        ).token
        _speech_config = speechsdk.SpeechConfig(endpoint=SPEECH_ENDPOINT)
        _speech_config.authorization_token = token
        _audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        _available = True
        log.info("Azure TTS initialised")
    except Exception as exc:
        log.warning("Azure TTS unavailable: %s", exc)
        _available = False


def speak_celebration(word, lang, phrase):
    """Speak the celebration sequence asynchronously: spell → word → phrase."""
    global _speaking
    _init()
    if not _available:
        return

    from config import TTS_VOICES
    import azure.cognitiveservices.speech as speechsdk

    voice = TTS_VOICES.get(lang)
    if not voice:
        return

    # Build the spelled-out form: "C. A. T."
    spelled = ". ".join(word) + "."

    with _lock:
        _speaking = True

    def _run():
        global _speaking
        try:
            _speech_config.speech_synthesis_voice_name = voice
            for text in (spelled, word, phrase):
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
