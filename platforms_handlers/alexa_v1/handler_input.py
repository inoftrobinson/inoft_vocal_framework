from collections import Callable

from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Response
from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict


class AlexaHandlerInput:
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    def __init__(self, parent_handler_input: HandlerInput):
        self.parent_handler_input = parent_handler_input
        self.session = Session()
        self.context = None
        self.request = Request()
        self.response = Response()

        self._is_new_session = None
        self._session_attributes = None

    @property
    def is_new_session(self) -> bool:
        if self._is_new_session is None:
            self._is_new_session = self.session.new if isinstance(self.session.new, bool) else False
        return self._is_new_session

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self,
                                                                  request_json_dict_stringed_dict_or_list=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])

    def _save_audio_on_pause_callback_function(self, on_pause_callback_function: Callable, identifier_key: str):
        self.parent_handler_input.save_callback_function_to_database(
            callback_functions_key_name="AudioPlayer_onPause_callbackFunctions",
            callback_function=on_pause_callback_function, identifier_key=identifier_key)

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

    # todo: create a new function that handle the end of a session (like an optionnal function in each class type ?)
    def say(self, text_or_ssml: str) -> None:
        self.response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        # todo: fix reprompt (for alexa and dialogflow)
        self.response.say_reprompt(text_or_ssml=text_or_ssml)

    def play_audio(self, identifier: str, on_pause_callback: Callable,  # on_end_callback: Callable,
                   mp3_file_url: str, title: str = None, subtitle: str = None,
                   icon_image_url: str = None, background_image_url: str = None,
                   milliseconds_start_offset: int = 0, override_default_end_session: bool = False):

        # todo: add all the callbacks

        self._save_audio_on_pause_callback_function(on_pause_callback_function=on_pause_callback, identifier_key=identifier)
        self.response.play_audio(identifier=identifier, mp3_file_url=mp3_file_url,
                                 title=title, subtitle=subtitle,
                                 icon_image_url=icon_image_url, background_image_url=background_image_url,
                                 milliseconds_start_offset=milliseconds_start_offset,
                                 override_default_end_session=override_default_end_session)

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

