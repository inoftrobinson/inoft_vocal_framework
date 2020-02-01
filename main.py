import json

from ask_sdk.standard import StandardSkillBuilder

from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftSkill
from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput
from inoft_vocal_framework.platforms_handlers.current_platform_static_data import *


def handle_any_platform(event: dict, context: dict, skill_builder: InoftSkill):
    print(f"Event = {event}\nContext = {context}")
    event_safedict = SafeDict(classic_dict=event)

    if event_safedict.get("resource").to_str() == "/google-assistant-v1":
        # A google-assistant or dialogflow request always pass trough an API gateway
        CurrentPlatformData.set_used_platform_id(RefsAvailablePlatforms.REF_PLATFORM_GOOGLE_ASSISTANT_V1)
    elif "amzn1." in event_safedict.get("context").get("System").get("application").get("applicationId").to_str():
        # Alexa always go last, since it do not pass trough an api resource, its a less robust identification than the other platforms.
        CurrentPlatformData.set_used_platform_id(RefsAvailablePlatforms.REF_PLATFORM_ALEXA_V1)
    else:
        from inoft_vocal_framework.messages import ERROR_PLATFORM_NOT_SUPPORTED
        raise Exception(ERROR_PLATFORM_NOT_SUPPORTED)

    handler_input = HandlerInput()
    handler_input.load_event_and_context(event=event, context=context)
    return skill_builder.process_request(handler_input=handler_input)


def convert_dialogflow_event(event):
    try:
        event = event["body"]
        event["version"] = "1.0"
        return event
    except:
        return dict()
