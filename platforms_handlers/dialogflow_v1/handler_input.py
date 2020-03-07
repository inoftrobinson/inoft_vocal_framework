from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import Response
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

