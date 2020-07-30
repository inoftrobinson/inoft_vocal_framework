from inoft_vocal_engine.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_engine.safe_dict import SafeDict


class Request:
    LaunchKeyName = "launch"

    class Context:
        def __init__(self):
            self._userId = None
            self._sessionId = None
            self._parameters = None

        @property
        def userId(self) -> str:
            return self._userId

        @userId.setter
        def userId(self, userId: str) -> None:
            raise_if_variable_not_expected_type(value=userId, expected_type=str, variable_name="userId")
            self._userId = userId

        @property
        def sessionId(self) -> str:
            return self._sessionId

        @sessionId.setter
        def sessionId(self, sessionId: str) -> None:
            raise_if_variable_not_expected_type(value=sessionId, expected_type=str, variable_name="sessionId")
            self._sessionId = sessionId

    def __init__(self):
        self._context = self.Context()
        self._intent = None
        self._parameters = None

    @property
    def context(self) -> Context:
        return self._context

    @property
    def intent(self) -> str:
        return self._intent

    @intent.setter
    def intent(self, intent: str) -> None:
        raise_if_variable_not_expected_type(value=intent, expected_type=str, variable_name="intent")
        self._intent = intent

    def is_launch_request(self):
        if self.intent == self.LaunchKeyName:
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list):
        if isinstance(intent_names_list, list):
            if self.intent.lower() in [name.lower() for name in intent_names_list]:
                return True
        elif isinstance(intent_names_list, str):
            if self.intent.lower() == intent_names_list.lower():
                return True
        return False

    def get_intent_parameter_value(self, parameter_key: str, default=None):
        return self.parameters.get(dict_key=parameter_key).to_any(default=default)

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


