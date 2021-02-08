import os
from typing import List
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


def render(audio_blocks: List[AudioBlock], out_filepath: str, out_format_type: str) -> str:
    path = os.path.dirname(os.path.abspath(__file__))
    print(path)
    os.add_dll_directory(path)
    from inoft_vocal_framework.audio_engine.audio_engine import render
    audio_blocks_data: List[dict] = list()
    for block in audio_blocks:
        audio_blocks_data.append(block.serialize())
    print(audio_blocks_data)

    """
    file_url: Optional[str] = None
    if engine_file_key is not None:
        account_id = "b1fe5939-032b-462d-92e0-a942cd445096"
        project_id = "22ac1d08-292d-4f2e-a9e3-20d181f1f58f"
        file_url = f"https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/{account_id}/{project_id}/files/{engine_file_key}.mp3"
        if full_file_url is not None:
            print("full_file_url not required and is being overridden by the engine_file_key")
    else:
        file_url = full_file_url
    """

    # todo: is the accountId and projectId's required ?
    data = {
        'engineAccountId': "b1fe5939-032b-462d-92e0-a942cd445096",
        'engineProjectId': "22ac1d08-292d-4f2e-a9e3-20d181f1f58f",
        'blocks': audio_blocks_data,
        'targetSpec': {
            'filepath': out_filepath,
            'sampleRate': 48000,
            'formatType': out_format_type,
            'exportTarget': 'managed-inoft-vocal-engine'  # 'local'
        },
    }
    return audio_engine.render(data)

