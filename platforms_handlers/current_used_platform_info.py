from typing import Optional

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type


class CurrentUsedPlatformInfo:
    PLATFORM_KEY_ALEXA = 'alexa'
    PLATFORM_KEY_DIALOGFLOW = 'dialogflow'
    PLATFORM_KEY_BIXBY = 'bixby'
    PLATFORM_KEY_DISCORD = 'discord'

    def __init__(self):
        self._platform: Optional[str] = None
        self._is_alexa = False
        self._is_dialogflow = False
        self._is_bixby = False
        self._is_discord = False

    @property
    def platform(self) -> str:
        return self._platform

    @platform.setter
    def platform(self, platform: str):
        if platform == self.PLATFORM_KEY_ALEXA:
            self.set_platform_to_alexa()
        elif platform == self.PLATFORM_KEY_DIALOGFLOW:
            self.set_platform_to_dialogflow()
        elif platform == self.PLATFORM_KEY_BIXBY:
            self.set_platform_to_bixby()
        elif platform == self.PLATFORM_KEY_DISCORD:
            self.set_platform_to_discord()
        else:
            raise Exception(f"Platform not supported : {platform}")

    def set_platform_to_alexa(self):
        self._platform = self.PLATFORM_KEY_ALEXA
        self._is_alexa = True
        self._is_dialogflow = False
        self._is_bixby = False
        self._is_discord = False

    def set_platform_to_dialogflow(self):
        self._platform = self.PLATFORM_KEY_DIALOGFLOW
        self._is_alexa = False
        self._is_dialogflow = True
        self._is_bixby = False
        self._is_discord = False

    def set_platform_to_bixby(self):
        self._platform = self.PLATFORM_KEY_BIXBY
        self._is_alexa = False
        self._is_dialogflow = False
        self._is_bixby = True
        self._is_discord = False

    def set_platform_to_discord(self):
        self._platform = self.PLATFORM_KEY_DISCORD
        self._is_alexa = False
        self._is_dialogflow = False
        self._is_bixby = False
        self._is_discord = True

    @property
    def is_alexa(self) -> bool:
        return self._is_alexa

    @property
    def is_dialogflow(self) -> bool:
        return self._is_dialogflow

    @property
    def is_bixby(self) -> bool:
        return self._is_bixby

    @property
    def is_discord(self) -> bool:
        return self._is_discord
