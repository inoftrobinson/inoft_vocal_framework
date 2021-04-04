import os
from typing import List, Union, Any, Dict
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


OUT_FORMATS_UNION = Union["mp3", "wav"]


def render(
    audio_blocks: List[AudioBlock], out_filepath: str, num_channels: int, sample_rate: int, bitrate: int,
    out_format_type: OUT_FORMATS_UNION, export_target='managed-inoft-vocal-engine'
) -> str:
    from inoft_vocal_framework.audio_engine import audio_engine
    audio_blocks_data: List[dict] = list()
    for block in audio_blocks:
        audio_blocks_data.append(block.serialize())

    # todo: is the accountId and projectId's required ?
    data = {
        'engineAccountId': "b1fe5939-032b-462d-92e0-a942cd445096",
        'engineProjectId': "22ac1d08-292d-4f2e-a9e3-20d181f1f58f",
        'blocks': audio_blocks_data,
        'targetSpec': {
            'filepath': out_filepath,
            'formatType': out_format_type,
            'sampleRate': sample_rate,
            'numChannels': num_channels,
            'bitrate': bitrate,
            'exportTarget': 'managed-inoft-vocal-engine'  # 'local'
            # todo: add support for local exportTarget
        },
    }
    return audio_engine.render(data)

def resample_save_file_from_url(
    file_url: str, out_filepath: str,
    num_channels: int, sample_rate: int, bitrate: int,
    out_format_type: OUT_FORMATS_UNION, export_target='local'
) -> Dict[str, Any]:
    # todo: add export_target support
    from inoft_vocal_framework.audio_engine import audio_engine
    data = {
        'fileUrl': file_url,
        'targetSpec': {
            'filepath': out_filepath,
            'numChannels': num_channels,
            'sampleRate': sample_rate,
            'bitrate': bitrate,
            'formatType': out_format_type,
            'exportTarget': export_target
        }
    }
    return audio_engine.resample_save_file_from_url(data)

def resample_save_file_from_local_file(
    source_filepath: str, out_filepath: str,
    num_channels: int, sample_rate: int, bitrate: int,
    out_format_type: OUT_FORMATS_UNION, export_target='local'
) -> bool:
    # todo: add export_target support
    from inoft_vocal_framework.audio_engine import audio_engine
    data = {
        'sourceFilepath': source_filepath,
        'targetSpec': {
            'filepath': out_filepath,
            'numChannels': num_channels,
            'sampleRate': sample_rate,
            'bitrate': bitrate,
            'formatType': out_format_type,
            'exportTarget': export_target
        }
    }
    return audio_engine.resample_save_file_from_local_file(data)

