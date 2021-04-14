from collections import Callable
from typing import Optional

from pydantic import PrivateAttr, Field
from pydantic.main import BaseModel

from inoft_vocal_framework.dummy_object import DummyObject
from inoft_vocal_framework.platforms_handlers.dialogflow.request import Request
from inoft_vocal_framework.platforms_handlers.dialogflow.response import Response, Image, ImageDisplayOptions
from inoft_vocal_framework.safe_dict import SafeDict
from json import loads as json_loads


class SurfaceCapabilities:
    CAN_PLAY_AUDIO_MEDIA = "actions.capability.MEDIA_RESPONSE_AUDIO"
    HAS_AN_OUTPUT_SPEAKER = "actions.capability.AUDIO_OUTPUT"
    CAN_POTENTIALLY_USE_ACCOUNT_LINKING = "actions.capability.ACCOUNT_LINKING"
    CAN_ACCESS_WEB_BROWSER = "actions.capability.WEB_BROWSER"
    HAS_A_SCREEN = "actions.capability.SCREEN_OUTPUT"

    ALL_CAPABILITIES = [
        CAN_PLAY_AUDIO_MEDIA,
        HAS_AN_OUTPUT_SPEAKER,
        CAN_POTENTIALLY_USE_ACCOUNT_LINKING,
        CAN_ACCESS_WEB_BROWSER,
        HAS_A_SCREEN,
    ]


class DialogFlowHandlerInput(BaseModel, SurfaceCapabilities):
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    request: Request

    _response: Response = PrivateAttr(default_factory=Response)
    _parent_handler_input: HandlerInput = PrivateAttr()
    _user_persistent_stored_data: Optional[dict] = PrivateAttr(default=None)
    _user_id: Optional[str] = PrivateAttr(default=None)
    _session_id: Optional[str] = PrivateAttr(default=None)
    _is_new_session: Optional[bool] = PrivateAttr(default=None)
    _simple_session_user_data: Optional[dict] = PrivateAttr(default=None)

    def __init__(self, parent_handler_input: HandlerInput, **kwargs):
        super().__init__(**kwargs)
        self._parent_handler_input = parent_handler_input

    @property
    def user_persistent_stored_data(self) -> dict:
        if self._user_persistent_stored_data is None:
            unprocessed_user_stored_data = self.request.originalDetectIntentRequest.payload.user.userStorage
            if isinstance(unprocessed_user_stored_data, str) and unprocessed_user_stored_data.replace(" ", "") != "":
                from unicodedata import normalize as unicode_normalize
                from ast import literal_eval
                try:
                    user_stored_data = literal_eval(unicode_normalize("NFD", unprocessed_user_stored_data))
                    if isinstance(user_stored_data, dict):
                        self._user_persistent_stored_data = user_stored_data
                    else:
                        print(f"Non-crashing error, the user_stored_data has been retrieved and converted from a string, but was but {type(user_stored_data)} and need to be a dict")
                except Exception as e:
                    print(f"Error while processing the user_persistent_data. Non-crashing but returning None : {e}")
        return self._user_persistent_stored_data

    def get_user_id(self) -> Optional[str]:
        return self.user_persistent_stored_data.get('userId', None) if self.user_persistent_stored_data is not None else None

    def get_updates_user_id(self) -> Optional[str]:
        return self.user_persistent_stored_data.get('updatesUserId', None) if self.user_persistent_stored_data is not None else None

    @property
    def session_id(self) -> str:
        if self._session_id is None:
            self._session_id = self.request.session
        return self._session_id

    @property
    def is_new_session(self) -> bool:
        if self._is_new_session is None:
            self._is_new_session = True if self.request.originalDetectIntentRequest.payload.conversation.type == "NEW" else False
        return self._is_new_session

    @property
    def simple_session_user_data(self) -> dict:
        for output_context in self.request.queryResult.outputContexts:
            if isinstance(output_context, dict) and 'name' in output_context.keys() and 'parameters' in output_context.keys():
                all_texts_after_slash = output_context['name'].split("/")
                last_text_after_slash = all_texts_after_slash[len(all_texts_after_slash) - 1]
                if str(last_text_after_slash).lower() == 'sessiondata':
                    # We lower the text, to make sure that it will work even if the cases have been lowered. Because for some reasons,
                    # google is lowering the keys, so even if the key in the framework os sessionData, google might return sessiondata.
                    parameters_stringed_dict_or_dict = output_context['parameters']
                    if parameters_stringed_dict_or_dict is not None:
                        if isinstance(parameters_stringed_dict_or_dict, str):
                            parameters_stringed_dict_or_dict = json_loads(parameters_stringed_dict_or_dict)
                        if isinstance(parameters_stringed_dict_or_dict, dict):
                            # The data key contains an stringed dictionary of the data we are interested by.
                            if 'data' in parameters_stringed_dict_or_dict.keys():
                                parameters_stringed_dict_or_dict = parameters_stringed_dict_or_dict['data']

                            if isinstance(parameters_stringed_dict_or_dict, str):
                                parameters_stringed_dict_or_dict = json_loads(parameters_stringed_dict_or_dict)
                            if isinstance(parameters_stringed_dict_or_dict, dict):
                                self._simple_session_user_data = parameters_stringed_dict_or_dict
                            else:
                                self._simple_session_user_data = {}
                        else:
                            raise Exception(f"parameters_stringed_dict_or_dict was nto None, not a str, dict and could"
                                            f"not be json converted to a dict : {parameters_stringed_dict_or_dict}")

        if not isinstance(self._simple_session_user_data, dict):
            self._simple_session_user_data = {}
        return self._simple_session_user_data

    def need_capabilities(self, capability_item_or_list):
        def check_if_capability_present_in_request(capability_to_check: str) -> bool:
            for capability_request_item in self.request.originalDetectIntentRequest.payload.surface.capabilities:
                if isinstance(capability_request_item, dict) and "name" in capability_request_item.keys():
                    if capability_request_item["name"] == capability_to_check:
                        return True
            return False

        if isinstance(capability_item_or_list, str):
            if (capability_item_or_list not in self.ALL_CAPABILITIES
            or check_if_capability_present_in_request(capability_to_check=capability_item_or_list) is False):
                return DummyObject()
            else:
                return self
        elif isinstance(capability_item_or_list, list):
            for capability_item in capability_item_or_list:
                if (capability_item not in self.ALL_CAPABILITIES
                or check_if_capability_present_in_request(capability_to_check=capability_item) is False):
                    return DummyObject()
            return self
        else:
            raise Exception(f"The variable passed to the need_capabilities function must be of type {list} or {str}"
                            f"but was {capability_item_or_list} of type {type(capability_item_or_list)}")

    def is_option_select_request(self) -> bool:
        return self.request.is_option_select_request()

    def selected_option_identifier(self) -> str:
        return self.request.selected_option_identifier()

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
        self._response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        self._response.say_reprompt(text_or_ssml=text_or_ssml)

    def show_suggestion_chips(self, chips_titles: list):
        self._response.add_suggestions_chips(chips_titles=chips_titles)

    def show_basic_card(
            self, title: str = None, subtitle: str = None, content_formatted_text: str = None,
            image: Image = None, image_display_options: ImageDisplayOptions = None, buttons: list = None
    ) -> None:
        if content_formatted_text is None and image is None:
            raise Exception("A google assistant basic card cannot have both the content_formatted_text and the image variable as None")

        from inoft_vocal_framework.platforms_handlers.dialogflow import BasicCard
        basic_card_object = BasicCard(
            title=title, subtitle=subtitle, formatted_text=content_formatted_text,
            image=image, image_display_options=image_display_options, buttons=buttons
        )
        self._response.add_response_item_to_show(item_object=basic_card_object)

    def show_browse_carousel_item(
            self, title: str, url_to_open_on_click: str, description: str = None,
            image_url: str = None, image_accessibility_text: str = None, footer: str = None
    ):
        self._response.add_item_to_browse_carousel(
            title=title, url_to_open_on_click=url_to_open_on_click, description=description,
            image_url=image_url, image_accessibility_text=image_accessibility_text, footer=footer
        )

    def _save_interaction_options_callback_function(self, on_select_callback_function: Callable, identifier_key: str):
        self._parent_handler_input.save_callback_function_to_database(
            callback_functions_key_name='interactivityCallbackFunctions',
            callback_function=on_select_callback_function, identifier_key=identifier_key
        )

    def show_interactive_list_item(
            self, identifier_key: str, on_select_callback: Callable, title: str, description: str = None,
            image_url: str = None, image_accessibility_text: str = None
    ):
        self._response.add_interactive_list_item_to_system_intent(
            identifier_key=identifier_key, item_title=title, item_description=description,
            item_image_url=image_url, item_image_accessibility_text=image_accessibility_text
        )
        self._save_interaction_options_callback_function(on_select_callback_function=on_select_callback, identifier_key=identifier_key)

    def show_interactive_carousel_item(
            self, identifier_key: str, on_select_callback: Callable, title: str, description: str,
            image_url: str = None, image_accessibility_text: str = None
    ):
        is_first_interactive_element = self._response.add_interactive_carousel_item_to_system_intent(
            identifier_key=identifier_key, item_title=title, item_description=description,
            item_image_url=image_url, item_image_accessibility_text=image_accessibility_text
        )
        self._save_interaction_options_callback_function(on_select_callback_function=on_select_callback, identifier_key=identifier_key)


    def play_audio(
            self, mp3_file_url: str, name: str, description: str = None,
            icon_image_url: str = None, icon_accessibility_text: str = None,
            override_default_end_session: bool = False
    ):

        self._response.add_item_to_audio_media_response(
            mp3_file_url=mp3_file_url, name=name, description=description,
            icon_image_url=icon_image_url, icon_accessibility_text=icon_accessibility_text
        )
        if override_default_end_session is False:
            self._parent_handler_input.end_session()

    def has_user_granted_push_notifications_permission(self) -> bool:
        user_permissions = self.request.originalDetectIntentRequest.payload.user.permissions
        if user_permissions is None or self.request.originalDetectIntentRequest.payload.user._PERMISSION_UPDATE_TYPE not in user_permissions:
            return False
        else:
            return True

    def request_push_notifications_permission_if_missing(self, intent_name: str) -> None:
        if not self.has_user_granted_push_notifications_permission():
            self._response.request_push_notifications_permission(intent_name=intent_name)

    def subscribe_current_user_to_notifications_group(self, group_key: str) -> bool:
        """:return True if the user has been able to be subscribed, False otherwise"""

        updates_user_id = self.get_updates_user_id()
        if updates_user_id is not None and self.has_user_granted_push_notifications_permission():
            self._parent_handler_input._notifications_subscribers_dynamodb_adapter.add_new_subscribed_group_to_user(
                updates_user_id=self.get_updates_user_id(), group_key=group_key
            )
            return True
        else:
            return False
