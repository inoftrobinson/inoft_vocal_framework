from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import Response, Image, ImageDisplayOptions
from inoft_vocal_framework.safe_dict import SafeDict
from json import loads as json_loads


class DialogFlowHandlerInput:
    def __init__(self):
        self.request = Request()
        self.response = Response()

        self._user_id = None
        self._session_id = None
        self._simple_session_user_data = None

    def _get_user_persistent_stored_data(self):
        unprocessed_user_stored_data = self.request.originalDetectIntentRequest.payload.user.userStorage
        if isinstance(unprocessed_user_stored_data, str) and unprocessed_user_stored_data.replace(" ", "") != "":
            from unicodedata import normalize as unicode_normalize
            from ast import literal_eval
            try:
                user_stored_data = literal_eval(unicode_normalize("NFD", unprocessed_user_stored_data))
                if isinstance(user_stored_data, dict):
                    return user_stored_data
                else:
                    print(f"Non-crashing error, the user_stored_data has been retrieved and converted from a string, but was but {type(user_stored_data)} and need to be a dict")
                    return None
            except Exception as e:
                print(f"Error while processing the user_persistent_data. Non-crashing but returning None : {e}")
        return None

    @property
    def user_id(self):
        persistent_data = self._get_user_persistent_stored_data()
        if isinstance(persistent_data, dict) and "userId" in persistent_data.keys():
            return persistent_data["userId"]
        else:
            return None

    @property
    def session_id(self) -> str:
        if self._session_id is None:
            self._session_id = self.request.session
        return self._session_id

    @property
    def simple_session_user_data(self) -> SafeDict:
        for output_context in self.request.queryResult.outputContexts:
            if isinstance(output_context, dict) and "name" in output_context.keys() and "parameters" in output_context.keys():
                all_texts_after_slash = output_context["name"].split("/")
                last_text_after_slash = all_texts_after_slash[len(all_texts_after_slash) - 1]
                if str(last_text_after_slash).lower() == "sessiondata":
                    # We lower the text, to make sure that it will work even if the cases have been lowered. Because for some reasons,
                    # google is lowering the keys, so even if the key in the framework os sessionData, google might return sessiondata.
                    parameters_stringed_dict_or_dict = output_context["parameters"]
                    if parameters_stringed_dict_or_dict is not None:
                        if isinstance(parameters_stringed_dict_or_dict, str):
                            parameters_stringed_dict_or_dict = json_loads(parameters_stringed_dict_or_dict)
                        if isinstance(parameters_stringed_dict_or_dict, dict):
                            # The data key contains an stringed dictionary of the data we are interested by.
                            if "data" in parameters_stringed_dict_or_dict.keys():
                                parameters_stringed_dict_or_dict = parameters_stringed_dict_or_dict["data"]

                            if isinstance(parameters_stringed_dict_or_dict, str):
                                parameters_stringed_dict_or_dict = json_loads(parameters_stringed_dict_or_dict)
                            if isinstance(parameters_stringed_dict_or_dict, dict):
                                self._simple_session_user_data = SafeDict(parameters_stringed_dict_or_dict)
                            else:
                                self._simple_session_user_data = SafeDict()
                        else:
                            raise Exception(f"parameters_stringed_dict_or_dict was nto None, not a str, dict and could"
                                            f"not be json converted to a dict : {parameters_stringed_dict_or_dict}")

        if not isinstance(self._simple_session_user_data, SafeDict):
            self._simple_session_user_data = SafeDict()
        return self._simple_session_user_data

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

    def show_suggestion_chips(self, chips_titles: list):
        self.response.add_suggestions_chips(chips_titles=chips_titles)

    def show_basic_card(self, title: str = None, subtitle: str = None, content_formatted_text: str = None,
                        image: Image = None, image_display_options: ImageDisplayOptions = None, buttons: list = None) -> None:

        if content_formatted_text is None and image is None:
            raise Exception("A google assistant basic card cannot have both the content_formatted_text and the image variable as None")

        from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import BasicCard
        basic_card_object = BasicCard(title=title, subtitle=subtitle, formatted_text=content_formatted_text,
                                      image=image, image_display_options=image_display_options, buttons=buttons)
        self.response.add_response_item_to_show(item_object=basic_card_object)

    def show_browse_carousel_item(self, title: str,  url_to_open_on_click: str, description: str = None,
                                  image_url: str = None, image_accessibility_text: str = None, footer: str = None):

        self.response.add_item_to_browse_carousel(title=title, url_to_open_on_click=url_to_open_on_click, description=description,
                                                  image_url=image_url, image_accessibility_text=image_accessibility_text, footer=footer)
