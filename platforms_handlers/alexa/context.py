from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_value_not_in_list


class Context:
    json_key = "context"

    class AudioPlayer:
        json_key = "AudioPlayer"
        PLAYER_ACTIVITY_STOPPED = "STOPPED"
        AVAILABLE_PLAYER_ACTIVITIES = [PLAYER_ACTIVITY_STOPPED]

        def __init__(self):
            self._offsetInMilliseconds = None
            self._token = None
            self._playerActivity = None

        @property
        def offsetInMilliseconds(self) -> int:
            return self._offsetInMilliseconds

        @offsetInMilliseconds.setter
        def offsetInMilliseconds(self, offsetInMilliseconds: int) -> None:
            raise_if_variable_not_expected_type(value=offsetInMilliseconds, expected_type=int, variable_name="offsetInMilliseconds")
            self._offsetInMilliseconds = offsetInMilliseconds

        @property
        def token(self) -> str:
            return self._token

        @token.setter
        def token(self, token: str) -> None:
            raise_if_variable_not_expected_type(value=token, expected_type=str, variable_name="token")
            self._token = token

        @property
        def playerActivity(self) -> str:
            return self._playerActivity

        @playerActivity.setter
        def playerActivity(self, playerActivity: str) -> None:
            raise_if_value_not_in_list(value=playerActivity, list_object=self.AVAILABLE_PLAYER_ACTIVITIES, variable_name="playerActivity")
            self._playerActivity = playerActivity

    class System:
        json_key = "System"

        class Application:
            json_key = "application"

            def __init__(self):
                self._applicationId = None

            @property
            def applicationId(self) -> str:
                return self._applicationId

            @applicationId.setter
            def applicationId(self, applicationId: str) -> None:
                raise_if_variable_not_expected_type(value=applicationId, expected_type=str, variable_name="applicationId")
                self._applicationId = applicationId

        class User:
            json_key = "user"

            def __init__(self):
                self._userId = None

            @property
            def userId(self) -> str:
                return self._userId

            @userId.setter
            def userId(self, userId: str) -> None:
                raise_if_variable_not_expected_type(value=userId, expected_type=str, variable_name="userId")
                self._userId = userId

        class Device:
            json_key = "device"

            class SupportedInterfaces:
                json_key = "supportedInterfaces"

                def __init__(self):
                    pass
                    # todo: complete the supported interfaces class

            def __init__(self):
                self._deviceId = None
                self.supportedInterfaces = self.SupportedInterfaces()

            @property
            def deviceId(self) -> str:
                return self._deviceId

            @deviceId.setter
            def deviceId(self, deviceId: str) -> None:
                raise_if_variable_not_expected_type(value=deviceId, expected_type=str, variable_name="deviceId")
                self._deviceId = deviceId

        def __init__(self):
            self.application = self.Application()
            self.user = self.User()
            self.device = self.Device()
            self._apiEndpoint = None
            self._apiAccessToken = None

        @property
        def apiEndpoint(self) -> str:
            return self._apiEndpoint

        @apiEndpoint.setter
        def apiEndpoint(self, apiEndpoint: str) -> None:
            raise_if_variable_not_expected_type(value=apiEndpoint, expected_type=str, variable_name="apiEndpoint")
            self._apiEndpoint = apiEndpoint

        @property
        def apiAccessToken(self) -> str:
            return self._apiAccessToken

        @apiAccessToken.setter
        def apiAccessToken(self, apiAccessToken: str) -> None:
            raise_if_variable_not_expected_type(value=apiAccessToken, expected_type=str, variable_name="apiAccessToken")
            self._apiAccessToken = apiAccessToken

    def __init__(self):
        self.audioPlayer = self.AudioPlayer()
        self.system = self.System()
