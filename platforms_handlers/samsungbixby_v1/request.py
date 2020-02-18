class Request:
    LaunchKeyName = "launch"

    def __init__(self):
        self._intent = str()
        self._userId = str()

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

    @property
    def intent(self) -> str:
        return self._intent

    @intent.setter
    def intent(self, intent: str) -> None:
        if not isinstance(intent, str):
            raise Exception(f"intent was type {type(intent)} which is not valid value for his parameter.")
        self._intent = intent

    @property
    def userId(self) -> str:
        return self._userId

    @userId.setter
    def userId(self, userId: str) -> None:
        if not isinstance(userId, str):
            raise Exception(f"userId was type {type(userId)} which is not valid value for his parameter.")
        self._userId = userId


