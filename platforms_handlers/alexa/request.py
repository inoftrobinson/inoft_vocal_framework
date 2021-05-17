from typing import List, Dict, Optional
from pydantic.main import BaseModel


class IntentSlot(BaseModel):
    value: str

class Intent(BaseModel):
    name: str
    confirmationStatus: str
    slots: Optional[Dict[str, IntentSlot]] = None


class Request(BaseModel):
    type: str
    requestId: str
    timestamp: str
    locale: str

    dialogState: Optional[str] = None
    intent: Optional[Intent] = None

    _LaunchRequestKeyName = 'LaunchRequest'
    _IntentRequestKeyName = 'IntentRequest'
    _SessionEndedRequestKeyName = 'SessionEndedRequest'

    def is_launch_request(self) -> bool:
        return self.type == self._LaunchRequestKeyName

    def active_intent_name(self) -> Optional[str]:
        if self.type == self._IntentRequestKeyName:
            formatted_intent_name = self.intent.name.lower()
            return formatted_intent_name
        return None

    def is_in_intent_names(self, intent_names_list: List[str] or str) -> bool:
        intent_name: Optional[str] = self.active_intent_name()
        if intent_name is None:
            return False

        if isinstance(intent_names_list, list):
            return intent_name in [name.lower() for name in intent_names_list]
        elif isinstance(intent_names_list, str):
            return intent_name == intent_names_list.lower()
        else:
            raise Exception(
                f"The intent_names_list must be a list or a str, but it was"
                f" a {type(intent_names_list)} object : {intent_names_list}"
            )

    def is_in_request_types(self, request_types_list: List[str] or str) -> bool:
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
        slot_item = self.intent.slots.get(slot_key, None)
        slot_value = slot_item.value if slot_item is not None else None
        # In Alexa, a ? as an arg value, means that it has not been specified
        return default if slot_value is None or slot_value == "?" else slot_value

    def do_not_include(self) -> bool:
        if self.type is not None and self.type not in [self._LaunchRequestKeyName, self._IntentRequestKeyName, self._SessionEndedRequestKeyName]:
            raise Exception(f"The request type '{self.type}' is not None or any of the supported types.")
        return False

