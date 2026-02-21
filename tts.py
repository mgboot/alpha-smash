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


def speak_word(word, lang):
    """Start speaking *word* asynchronously.  Returns immediately."""
    global _speaking
    _init()
    if not _available:
        return

    from config import TTS_VOICES
    import azure.cognitiveservices.speech as speechsdk

    voice = TTS_VOICES.get(lang)
    if not voice:
        return

    _speech_config.speech_synthesis_voice_name = voice

    with _lock:
        _speaking = True

    def _run():
        global _speaking
        try:
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=_speech_config,
                audio_config=_audio_config,
            )
            result = synthesizer.speak_text_async(word).get()
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
