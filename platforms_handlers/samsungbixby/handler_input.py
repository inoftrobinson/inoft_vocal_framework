from typing import List

from inoft_vocal_framework.platforms_handlers.samsungbixby.request import Request
from inoft_vocal_framework.platforms_handlers.samsungbixby.response import Response


class BixbyHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input
        self.request = Request()
        self.response = Response()

    def is_launch_request(self) -> bool:
        return self.request.is_launch_request()

    def is_in_intent_names(self, intent_names_list: List[str] or str) -> bool:
        return self.request.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str) -> None:
        self.response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        self.response.say_reprompt(text_or_ssml=text_or_ssml)


