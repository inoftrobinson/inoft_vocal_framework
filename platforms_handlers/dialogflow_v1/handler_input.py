from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import Response, SimpleResponse


class DialogFlowHandlerInput:
    def __init__(self):
        self.request = Request()
        self.response = Response()

    def get_user_persistent_data(self):
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

    def get_user_id(self):
        persistent_data = self.get_user_persistent_data()
        if not isinstance(persistent_data, dict) or "userId" not in persistent_data.keys():
            return None
        else:
            return persistent_data["userId"]
