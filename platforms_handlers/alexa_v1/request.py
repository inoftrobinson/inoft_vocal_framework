from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict


class IntentSlot:
    def __init__(self):
        pass

class Intent:
    json_key = "intent"

    def __init__(self):
        self._name = str()
        self._confirmationStatus = str()
        self._slots = SafeDict()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception(f"name was type {type(name)} which is not valid value for his parameter.")
        self._name = name

    @property
    def confirmationStatus(self) -> str:
        return self._confirmationStatus

    @confirmationStatus.setter
    def confirmationStatus(self, confirmationStatus: str) -> None:
        if not isinstance(confirmationStatus, str):
            raise Exception(f"confirmationStatus was type {type(confirmationStatus)} which is not valid value for his parameter.")
        self._confirmationStatus = confirmationStatus

    @property
    def slots(self) -> SafeDict:
        if isinstance(self._slots, dict):
            self._slots = SafeDict(self._slots)
        return self._slots

    @slots.setter
    def slots(self, slots: dict) -> None:
        if not isinstance(slots, dict):
            raise Exception(f"slots was type {type(slots)} which is not valid value for his parameter.")
        self._slots = SafeDict(slots)

class Request:
    json_key = "request"

    LaunchRequestKeyName = "LaunchRequest"
    IntentRequestKeyName = "IntentRequest"
    SessionEndedRequestKeyName = "SessionEndedRequest"

    def __init__(self):
        # General for LaunchRequest, IntentRequest and SessionEndedRequest
        self._type = str()
        self._requestId = str()
        self._timestamp = str()
        self._locale = str()

        # Only for an IntentRequest
        self._dialogState = None
        self._intent = Intent()

    def process_and_set_json_to_object(self, stringed_request_json_dict: str):
        NestedObjectToDict.process_and_set_json_to_object(object_class_to_set_to=self,
                                                          request_json_dict_stringed_dict_or_list=stringed_request_json_dict)

    def is_launch_request(self) -> bool:
        if self.type == self.LaunchRequestKeyName:
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list) -> bool:
        if self.type == self.IntentRequestKeyName:
            if isinstance(intent_names_list, list):
                if self.intent.name in intent_names_list:
                    return True
            elif isinstance(intent_names_list, str):
                if self.intent.name == intent_names_list:
                    return True
            else:
                raise Exception(f"The intent_names_list must be a list or a str, but it was"
                                f" a {type(intent_names_list)} object : {intent_names_list}")
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

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_value: str) -> None:
        if not isinstance(type_value, str):
            raise Exception(f"type_value must be a str object : {type_value}")
        self._type = type

    @property
    def requestId(self):
        return self._requestId

    @requestId.setter
    def requestId(self, request_id: str) -> None:
        if not isinstance(request_id, str):
            raise Exception(f"request_id must be a str object : {request_id}")
        self._requestId = request_id

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: str) -> None:
        if not isinstance(timestamp, str):
            raise Exception(f"timestamp must be a str object : {timestamp}")
        self._timestamp = timestamp

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, locale: str) -> None:
        if not isinstance(locale, str):
            raise Exception(f"locale must be a str object : {locale}")
        self._locale = locale

    @property
    def dialogState(self):
        return self._dialogState

    @dialogState.setter
    def dialogState(self, dialog_state: str) -> None:
        if not isinstance(dialog_state, str):
            raise Exception(f"dialog_state must be a str object : {dialog_state}")
        self._dialogState = dialog_state

    @property
    def intent(self):
        return self._intent

    @intent.setter
    def intent(self, intent: str) -> None:
        if not isinstance(intent, str):
            raise Exception(f"intent must be a str object : {intent}")
        self._intent = intent

    def to_dict(self) -> dict:
        dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                                     key_names_identifier_objects_to_go_into=["json_key"])
        dict_object["version"] = "1.0"
        dict_object["sessionAttributes"] = dict()
        return dict_object
