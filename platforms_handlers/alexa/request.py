from dataclasses import dataclass
from typing import List, Dict, Optional

from pydantic.main import BaseModel

from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict


class IntentSlot(BaseModel):
    pass

class Intent(BaseModel):
    json_key = "intent"

    name: str
    confirmationStatus: str
    slots: Dict[str, IntentSlot]


class Request(BaseModel):
    type: str
    requestId: str
    timestamp: str
    locale: str

    dialogState: Optional[str] = None
    intent: Optional[Intent] = None

    LaunchRequestKeyName = "LaunchRequest"
    IntentRequestKeyName = "IntentRequest"
    SessionEndedRequestKeyName = "SessionEndedRequest"

    def process_and_set_json_to_object(self, stringed_request_json_dict: str):
        NestedObjectToDict.process_and_set_json_to_object(object_class_to_set_to=self,
                                                          request_json_dict_stringed_dict_or_list=stringed_request_json_dict)

    def is_launch_request(self) -> bool:
        return self.type == self.LaunchRequestKeyName

    def is_in_intent_names(self, intent_names_list: List[str] or str) -> bool:
        if self.type == self.IntentRequestKeyName:
            formatted_intent_name = self.intent.name.lower()
            if isinstance(intent_names_list, list):
                return formatted_intent_name in [name.lower() for name in intent_names_list]
            elif isinstance(intent_names_list, str):
                return formatted_intent_name == intent_names_list.lower()
            else:
                raise Exception(
                    f"The intent_names_list must be a list or a str, but it was"
                    f" a {type(intent_names_list)} object : {intent_names_list}"
                )
        return False

    def is_in_request_types(self, request_types_list) -> bool:
        if isinstance(request_types_list, list):
            if self.type in request_types_list:
                return True
        elif isinstance(request_types_list, str):
            if self.type == request_types_list:
                return True
        else:
            raise Exception(f"The request_types_list must be a list or a str, but it was"
                            f" a {type(request_types_list)} object : {request_types_list}")
        return False

    def get_intent_slot_value(self, slot_key: str, default=None):
        slot_value = self.intent.slots.get(dict_key=slot_key).get("value").to_any(default=default)
        # In Alexa, a ? as an arg value, means that it has not been specified
        return default if slot_value == "?" else slot_value

    def do_not_include(self) -> bool:
        if self.type is not None and self.type not in [self.LaunchRequestKeyName, self.IntentRequestKeyName, self.SessionEndedRequestKeyName]:
            raise Exception(f"The request type '{self.type}' is not None or any of the supported types.")

        return False
        if (self._type == str()
        or self._requestId == str()
        or self._timestamp == str()
        or self._locale == str()):
            return True
        else:
            return False

    def to_dict(self) -> dict:
        dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                                     key_names_identifier_objects_to_go_into=["json_key"])
        dict_object["version"] = "1.0"
        dict_object["sessionAttributes"] = dict()
        return dict_object
