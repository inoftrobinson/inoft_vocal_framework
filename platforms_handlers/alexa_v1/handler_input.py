from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request
from inoft_vocal_framework.platforms_handlers.alexa_v1.response.response import Response
from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict


class AlexaHandlerInput:
    def __init__(self):
        self.session = Session()
        self.context = None
        self.request = Request()
        self.response = Response()

    def load_event_and_context(self, event: dict, context: dict):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self,
                                                                  request_json_dict_or_stringed_dict=event,
                                                                  key_names_identifier_objects_to_go_into=["json_key"])

