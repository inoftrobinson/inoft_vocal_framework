from inoft_vocal_framework.audio_editing.base_audio_effect import BaseAudioEffect
from dataclasses import dataclass


@dataclass
class EqualizerEffect(BaseAudioEffect):
    _KEY = 'equalizer'

