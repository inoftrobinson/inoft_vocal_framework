from inoft_vocal_framework.audio_editing.base_audio_effect import BaseAudioEffect
from dataclasses import dataclass


@dataclass
class TremoloEffect(BaseAudioEffect):
    _KEY = 'tremolo'
    gain: float
    speed: float
