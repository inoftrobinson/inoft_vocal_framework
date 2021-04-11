from typing import Callable, Dict
from StructNoSQL.practical_logger import message_with_vars
from inoft_vocal_framework import Settings, InoftSkill
from inoft_vocal_framework.audio_editing.sound import Sound


def _api_speech_synthesis_handler(api_base_url: str, text: str, voice_key: str, base_sound_kwargs: dict) -> Sound:
    import requests
    # todo: stop using a static account
    response = requests.post(
        url=f"{api_base_url}/api/v1/@robinsonlabourdette/livetiktok/resources/project-audio-files/synthesise-get-dialogue",
        json={'text': text, 'metadata': {'voiceKey': voice_key}}
    )
    data = response.json()
    if data['protocol'] == 'bytes':
        from base64 import b64decode
        decoded_bytes = b64decode(data['bytes'])
        return Sound(file_bytes=decoded_bytes, **base_sound_kwargs)
    elif data['protocol'] == 'url':
        file_url = data['url']
        return Sound(file_url=file_url, **base_sound_kwargs)
    else:
        raise Exception(message_with_vars(message="Protocol not supported", vars_dict={'protocol': data['protocol']}))

def _online_engine_handler(text: str, voice_key: str, base_sound_kwargs: dict):
    return _api_speech_synthesis_handler(api_base_url='https://www.engine.inoft.com', text=text, voice_key=voice_key, base_sound_kwargs=base_sound_kwargs)

def _next_engine_handler(text: str, voice_key: str, base_sound_kwargs: dict):
    return _api_speech_synthesis_handler(api_base_url='https://www.next.engine.inoft.com', text=text, voice_key=voice_key, base_sound_kwargs=base_sound_kwargs)

def _local_engine_handler(text: str, voice_key: str, base_sound_kwargs: dict):
    return _api_speech_synthesis_handler(api_base_url='http://127.0.0.1:5000', text=text, voice_key=voice_key, base_sound_kwargs=base_sound_kwargs)

def _provided_aws_handler(text: str, voice_key: str, base_sound_kwargs: dict):
    # todo: allow a method to use boto3 instead of the engine API
    raise Exception("Not yet implement")


SPEECH_SYNTHESIS_HANDLERS_SWITCH: Dict[str, Callable[[str, str, dict], Sound]] = {
    Settings.INFRASTRUCTURE_ENGINE: _online_engine_handler,
    Settings.INFRASTRUCTURE_NEXT_ENGINE: _next_engine_handler,
    Settings.INFRASTRUCTURE_LOCAL_ENGINE: _local_engine_handler,
    Settings.INFRASTRUCTURE_PROVIDED_AWS: _provided_aws_handler
}
def get_handler():
    handler = SPEECH_SYNTHESIS_HANDLERS_SWITCH.get(InoftSkill.APP_SETTINGS.infrastructure_speech_synthesis, None)
    if handler is None:
        raise Exception(f"No handler found for {InoftSkill.APP_SETTINGS.infrastructure_speech_synthesis}")
    return handler
