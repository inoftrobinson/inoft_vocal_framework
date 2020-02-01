from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict


class HandlerInput:
    def __init__(self):
        self._session = None
        self._context = None
        self._request = Request()

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self, request_json_dict_or_stringed_dict=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])

    def is_launch_request(self):
        if self.request.type == self.request.LaunchRequestKeyName:
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list):
        if self.request.type == self.request.IntentRequestKeyName:
            if isinstance(intent_names_list, list):
                if self.request.intent.name in intent_names_list:
                    return True
            elif isinstance(intent_names_list, str):
                if self.request.intent.name == intent_names_list:
                    return True
        return False

    @property
    def request(self):
        return self._request
