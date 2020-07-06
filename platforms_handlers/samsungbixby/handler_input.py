from inoft_vocal_engine.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_engine.platforms_handlers.samsungbixby.request import Request
from inoft_vocal_engine.platforms_handlers.samsungbixby.response import Response


class BixbyHandlerInput:
    from inoft_vocal_engine.platforms_handlers.handler_input import HandlerInput

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input
        self.request = Request()
        self.response = Response()

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
        self.response.say_reprompt(text_or_ssml=text_or_ssml)


