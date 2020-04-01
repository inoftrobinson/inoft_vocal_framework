from collections import Callable

from inoft_vocal_framework.platforms_handlers.alexa_v1.audioplayer.audioplayer_directives import AudioPlayerWrapper
from inoft_vocal_framework.platforms_handlers.alexa_v1.context import Context
from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Response
from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.safe_dict import SafeDict


class AlexaHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input
        self.session = Session()
        self.context = Context()
        self.request = Request()
        self.response = Response()

        self._is_new_session = None
        self._session_attributes = None
        self._audioplayer = None

    @property
    def is_new_session(self) -> bool:
        if self._is_new_session is None:
            self._is_new_session = self.session.new if isinstance(self.session.new, bool) else False
        return self._is_new_session

    def is_launch_request(self) -> bool:
        return self.request.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        return self.request.is_in_intent_names(intent_names_list=intent_names_list)

    def is_in_request_types(self, request_types_list: list):
        return self.request.is_in_request_types(request_types_list=request_types_list)

    # todo: create a new function that handle the end of a session (like an optionnal function in each class type ?)
    def say(self, text_or_ssml: str) -> None:
        self.response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        # todo: fix reprompt (for alexa and dialogflow)
        self.response.say_reprompt(text_or_ssml=text_or_ssml)

    @property
    def audioplayer(self) -> AudioPlayerWrapper:
        if self._audioplayer is None:
            self._audioplayer = AudioPlayerWrapper(parent_handler_input=self.parent_handler_input)
        return self._audioplayer

    def save_audioplayer_handlers_group_class(self, handlers_group_class_type: type, group_class_kwargs: dict = None):
        from inspect import getfile
        # We use the persistent attributes and not the session, because after launching an audio file with the audio player,
        # the session of the user will end. Then when interacting with an audio file there will be no session id.
        # So, if we save this data as session attributes, it would be considered of the same session only if the smart
        # session timeout has not been exceeded. Which is not at all what we want.
        self.parent_handler_input.persistent_memorize(data_key="lastUsedAudioPlayerHandlersGroupClass",
                                                      data_value={
                                                          "fileFilepathContainingClass": getfile(handlers_group_class_type),
                                                          "classPath": handlers_group_class_type.__qualname__,
                                                          "classKwargs": group_class_kwargs,
                                                      })

    def get_last_used_audioplayer_handlers_group(self) -> SafeDict:
        return SafeDict(self.parent_handler_input.persistent_remember("lastUsedAudioPlayerHandlersGroupClass", specific_object_type=dict))

    def show_basic_card(self, title: str, text: str, small_image_url: str = None, large_image_url: str = None) -> None:
        from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Card
        if small_image_url is not None or large_image_url is not None:
            from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Image

            if small_image_url is None and large_image_url is not None:
                small_image_url = large_image_url
                print("WARNING ! The small_image_url argument was not specified, the large_image_url"
                      "argument (which has been specified) is now also used as the small_image_url.")
            elif large_image_url is None and small_image_url is not None:
                large_image_url = small_image_url
                print("WARNING ! The large_image_url argument was not specified, the small_image_url"
                      "argument (which has been specified) is now also used as the large_image_url.")

            self.response.card = Card(type_value=Card.type_standard, title=title, text=text,
                                      image=Image(small_image_url=small_image_url, large_image_url=large_image_url))
        else:
            self.response.card = Card(type_value=Card.type_simple, title=title, content_text=text)

    def show_link_account_card(self) -> None:
        raise Exception("Not yet implemented")

    def show_ask_permissions_card(self) -> None:
        raise Exception("Not yet implemented")

    def end_session(self, should_end: bool = True) -> None:
        self.response.end_session(should_end=should_end)

    @property
    def session_attributes(self) -> SafeDict:
        if not isinstance(self._session_attributes, SafeDict):
            if isinstance(self.session.attributes, dict):
                self._session_attributes = SafeDict(self.session.attributes)
            else:
                self._session_attributes = SafeDict()
        return self._session_attributes

