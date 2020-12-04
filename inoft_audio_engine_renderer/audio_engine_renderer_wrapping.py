from typing import List
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


def render(audio_blocks: List[AudioBlock]) -> str:
    from inoft_vocal_framework.inoft_audio_engine_renderer.inoft_audio_engine_renderer import render
    audio_blocks_data: List[dict] = list()
    for block in audio_blocks:
        audio_blocks_data.append(block.serialize())
    print(audio_blocks_data)

    data = {
        'blocks': audio_blocks_data,
        'targetSpec': {
            'sampleRate': 48000
        }
    }
    return render(data)

