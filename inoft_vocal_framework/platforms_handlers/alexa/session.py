class Session:
    json_key = "session"

    def __init__(self):
        self._new = bool()
        self._sessionId = str()
        self._application = dict()
        self._user = dict()
        self._attributes = dict()

    @property
    def new(self):
        return self._new

    @new.setter
    def new(self, new: bool) -> None:
        if not isinstance(new, bool):
            raise Exception(f"new was type {type(new)} which is not valid value for his parameter.")
        self._new = new

    @property
    def sessionId(self) -> str:
        return self._sessionId

    @sessionId.setter
    def sessionId(self, sessionId: str) -> None:
        if not isinstance(sessionId, str):
            raise Exception(f"sessionId was type {type(sessionId)} which is not valid value for his parameter.")
        self._sessionId = sessionId

    @property
    def application(self) -> dict:
        return self._application

    @application.setter
    def application(self, application: dict) -> None:
        if not isinstance(application, dict):
            raise Exception(f"application was type {type(application)} which is not valid value for his parameter.")
        self._application = application

    @property
    def user(self) -> dict:
        return self._user

    @user.setter
    def user(self, user: dict) -> None:
        if not isinstance(user, dict):
            raise Exception(f"user was type {type(user)} which is not valid value for his parameter.")
        self._user = user

    @property
    def attributes(self) -> dict:
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: dict) -> None:
        if not isinstance(attributes, dict):
            raise Exception(f"attributes was type {type(attributes)} which is not valid value for his parameter.")
        self._attributes = attributes
