from inoft_vocal_framework.safe_dict import SafeDict


class Request:
    LaunchKeyName = "launch"

    def __init__(self):
        self._userId = str()
        self._sessionId = str()
        self._intent = str()
        self._parameters = SafeDict()

    def is_launch_request(self):
        if self.intent == self.LaunchKeyName:
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list):
        if isinstance(intent_names_list, list):
            if self.intent in intent_names_list:
                return True
        elif isinstance(intent_names_list, str):
            if self.intent == intent_names_list:
                return True
        return False

    def get_intent_parameter_value(self, parameter_key: str, default=None):
        return self.parameters.get(dict_key=parameter_key).to_any(default=default)

    @property
    def userId(self) -> str:
        return self._userId

    @userId.setter
    def userId(self, userId: str) -> None:
        if not isinstance(userId, str):
            raise Exception(f"userId was type {type(userId)} which is not valid value for his parameter.")
        self._userId = userId

    @property
    def sessionId(self) -> str:
        return self._sessionId

    @sessionId.setter
    def sessionId(self, sessionId: str) -> None:
        if not isinstance(sessionId, str):
            raise Exception(f"sessionId was type {type(sessionId)} which is not valid value for his parameter.")
        self._sessionId = sessionId

    @property
    def intent(self) -> str:
        return self._intent

    @intent.setter
    def intent(self, intent: str) -> None:
        if not isinstance(intent, str):
            raise Exception(f"intent was type {type(intent)} which is not valid value for his parameter.")
        self._intent = intent

    @property
    def parameters(self) -> SafeDict:
        if isinstance(self._parameters, dict):
            self._parameters = SafeDict(self._parameters)
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: dict) -> None:
        if not isinstance(parameters, dict):
            raise Exception(f"parameters was type {type(parameters)} which is not valid value for his parameter.")
        self._parameters = SafeDict(parameters)


