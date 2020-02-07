from inoft_vocal_framework.utils import get_dict_of_all_custom_defined_variables_of_class

class CurrentPlatformData:
    used_platform_id = None
    _is_alexa_v1 = False
    _is_dialogflow_v1 = False

    @property
    def is_alexa_v1(self) -> bool:
        return self._is_alexa_v1

    @is_alexa_v1.setter
    def is_alexa_v1(self, is_alexa_v1: bool) -> None:
        if not isinstance(is_alexa_v1, bool):
            raise Exception(f"is_alexa_v1 was type {type(is_alexa_v1)} which is not valid value for his parameter.")
        self._is_alexa_v1 = is_alexa_v1

    @property
    def is_dialogflow_v1(self) -> bool:
        return self._is_dialogflow_v1

    @is_dialogflow_v1.setter
    def is_dialogflow_v1(self, is_dialogflow_v1: bool) -> None:
        if not isinstance(is_dialogflow_v1, bool):
            raise Exception(f"is_dialogflow_v1 was type {type(is_dialogflow_v1)} which is not valid value for his parameter.")
        self._is_dialogflow_v1 = is_dialogflow_v1

class SessionInfo:
    session_id = str()
