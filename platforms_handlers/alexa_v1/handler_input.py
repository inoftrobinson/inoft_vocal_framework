from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.alexa_v1.response import Response
from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict


class AlexaHandlerInput:
    session = Session()
    context = None
    request = Request()
    response = Response()

    @staticmethod
    def load_event_and_context(event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=AlexaHandlerInput,
                                                                  request_json_dict_or_stringed_dict=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])
        
    @staticmethod
    def is_launch_request():
        if AlexaHandlerInput.request.type == AlexaHandlerInput.request.LaunchRequestKeyName:
            return True
        else:
            return False

    @staticmethod
    def is_in_intent_names(intent_names_list):
        if AlexaHandlerInput.request.type == AlexaHandlerInput.request.IntentRequestKeyName:
            if isinstance(intent_names_list, list):
                if AlexaHandlerInput.request.intent.name in intent_names_list:
                    return True
            elif isinstance(intent_names_list, str):
                if AlexaHandlerInput.request.intent.name == intent_names_list:
                    return True
        return False

    @staticmethod
    def say(text_or_ssml: str):
        is_ssml = False
        if "<speak>" in text_or_ssml:
            # For ssml, the speak balise must start the string, so if we find other chars than
            # whitespaces before the balise, we consider that the string to not be a ssml string.
            before_start_balise, after_start_balise = text_or_ssml.split("<speak>", maxsplit=1)
            are_all_chars_in_before_start_balise_whitespaces = True
            for char in before_start_balise:
                if char != " ":
                    are_all_chars_in_before_start_balise_whitespaces = False
            if are_all_chars_in_before_start_balise_whitespaces is True:
                is_ssml = True

        if is_ssml is True:
            AlexaHandlerInput.response.outputSpeech.set_ssml(ssml_string=text_or_ssml)
        else:
            AlexaHandlerInput.response.outputSpeech.set_text(text=text_or_ssml)
