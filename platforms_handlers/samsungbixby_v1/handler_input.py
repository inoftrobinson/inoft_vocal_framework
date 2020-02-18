from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.platforms_handlers.samsungbixby_v1.request import Request
from inoft_vocal_framework.platforms_handlers.samsungbixby_v1.response import Response


class BixbyHandlerInput:
    def __init__(self):
        self.request = Request()
        self.response = Response()

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self.request,
                                                                  request_json_dict_or_stringed_dict=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])

