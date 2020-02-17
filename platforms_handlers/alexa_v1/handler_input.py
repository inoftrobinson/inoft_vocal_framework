from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Response
from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict


class AlexaHandlerInput:
    def __init__(self):
        self.session = Session()
        self.context = None
        self.request = Request()
        self.response = Response()

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self,
                                                                  request_json_dict_or_stringed_dict=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])
        
    def is_launch_request(self):
        if self.request.type == self.request.LaunchRequestKeyName:
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list):
        if self.request.type == self.request.IntentRequestKeyName:
            if isinstance(intent_names_list, list):
                if self.request.intent.name in intent_names_list:
                    return True
            elif isinstance(intent_names_list, str):
                if self.request.intent.name == intent_names_list:
                    return True
        return False

    def is_text_ssml(self, text_or_ssml: str):
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
        return is_ssml

    def say(self, text_or_ssml: str):
        is_ssml = self.is_text_ssml(text_or_ssml=text_or_ssml)

        if is_ssml is True:
            self.response.outputSpeech.set_ssml(ssml_string=text_or_ssml)
        else:
            self.response.outputSpeech.set_text(text=text_or_ssml)

    def reprompt(self, text_or_ssml: str):
        is_ssml = self.is_text_ssml(text_or_ssml=text_or_ssml)

        if is_ssml is True:
            self.response.reprompt.outputSpeech.set_ssml(ssml_string=text_or_ssml)
        else:
            self.response.reprompt.outputSpeech.set_text(text=text_or_ssml)
