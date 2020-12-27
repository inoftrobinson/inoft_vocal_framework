from typing import List
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.nodes.collection.audio_block import AudioBlockNode


def render(audio_blocks: List[AudioBlock or AudioBlockNode], out_filepath: str, out_format_type: str) -> str:
    from inoft_vocal_framework.inoft_audio_engine_renderer.inoft_audio_engine_renderer import render
    audio_blocks_data: List[dict] = list()
    for block in audio_blocks:
        audio_blocks_data.append(block.serialize())
    print(audio_blocks_data)

    data = {
        'blocks': audio_blocks_data,
        'targetSpec': {
            'filepath': out_filepath,
            'sampleRate': 48000,
            'formatType': out_format_type,
            'exportTarget': 'managed-inoft-vocal-engine'  # 'local'
        },
    }
    return render(data)

