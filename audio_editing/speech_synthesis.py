from typing import Callable, Dict, Optional
from StructNoSQL.practical_logger import message_with_vars
from inoft_vocal_framework import Settings, InoftSkill
from inoft_vocal_framework.audio_editing.sound import Sound


def _api_speech_synthesis_handler(api_base_url: str, text: str, voice_key: str, base_sound_kwargs: dict) -> Optional[Sound]:
    # todo: migrate to rust backend ?
    import requests
    base_api_project_url = f"{api_base_url}/api/v1/{InoftSkill.APP_SETTINGS.engine_account_id}/{InoftSkill.APP_SETTINGS.engine_project_id}"
    response = requests.post(
        url=f"{base_api_project_url}/resources/project-audio-files/synthesise-get-dialogue",
        json={'accessToken': InoftSkill.APP_SETTINGS.engine_api_key, 'text': text, 'metadata': {'voiceKey': voice_key}}
    )
    response_data: Optional[dict] = response.json()
    if response_data is None:
        return None

    success: bool = response_data.get('success', False)
    if success is not True:
        print("Speech synthesis - Success was not True")
        return None

    protocol: Optional[str] = response_data.get('protocol', None)
    if protocol is None:
        print("Speech synthesis - Missing protocol key")
        return None

    if protocol == 'bytes':
        from base64 import b64decode
        encoded_bytes: Optional[str] = response_data.get('bytes', None)
        if encoded_bytes is None:
            print("Speech synthesis - Missing bytes key with the bytes protocol")
            return None
        decoded_bytes: bytes = b64decode(encoded_bytes)
        return Sound(file_bytes=decoded_bytes, **base_sound_kwargs)

    elif protocol == 'url':
        file_url: Optional[str] = response_data.get('url', None)
        if file_url is None:
            print("Speech synthesis - Missing url key with the url protocol")
            return None
        return Sound(file_url=file_url, **base_sound_kwargs)

    else:
        raise Exception(message_with_vars(message="Protocol not supported", vars_dict={'protocol': protocol}))

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
