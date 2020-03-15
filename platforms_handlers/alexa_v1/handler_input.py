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

        self._session_attributes = None

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self,
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

    @property
    def session_attributes(self) -> SafeDict:
        if not isinstance(self._session_attributes, SafeDict):
            if isinstance(self.session.attributes, dict):
                self._session_attributes = SafeDict(self.session.attributes)
            else:
                self._session_attributes = SafeDict()
        return self._session_attributes

