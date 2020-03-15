from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.platforms_handlers.samsungbixby_v1.request import Request
from inoft_vocal_framework.platforms_handlers.samsungbixby_v1.response import Response


class BixbyHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input
        self.request = Request()
        self.response = Response()

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self.request,
                                                                  request_json_dict_stringed_dict_or_list=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])

    def is_launch_request(self) -> bool:
        return self.request.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        if not isinstance(intent_names_list, list):
            if isinstance(intent_names_list, str):
                intent_names_list = [intent_names_list]
            else:
                raise Exception(f"The intent_names_list must be a list or a str in order to be converted to a list,"
                                f"but it was a {type(intent_names_list)} object : {intent_names_list}")

        return self.request.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str) -> None:
        self.response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        self.response.reprompt(text_or_ssml=text_or_ssml)


