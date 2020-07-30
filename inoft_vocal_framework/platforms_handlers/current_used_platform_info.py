from inoft_vocal_engine.exceptions import raise_if_variable_not_expected_type


class CurrentUsedPlatformInfo:
    def __init__(self):
        self._is_alexa = False
        self._is_dialogflow = False
        self._is_bixby = False
        self._is_discord = False

    @property
    def is_alexa(self) -> bool:
        return self._is_alexa

    @is_alexa.setter
    def is_alexa(self, is_alexa: bool) -> None:
        raise_if_variable_not_expected_type(value=is_alexa, expected_type=bool, variable_name="is_alexa")
        self._is_alexa = is_alexa

    @property
    def is_dialogflow(self) -> bool:
        return self._is_dialogflow

    @is_dialogflow.setter
    def is_dialogflow(self, is_dialogflow: bool) -> None:
        raise_if_variable_not_expected_type(value=is_dialogflow, expected_type=bool, variable_name="is_dialogflow")
        self._is_dialogflow = is_dialogflow

    @property
    def is_bixby(self) -> bool:
        return self._is_bixby

    @is_bixby.setter
    def is_bixby(self, is_bixby: bool) -> None:
        raise_if_variable_not_expected_type(value=is_bixby, expected_type=bool, variable_name="is_bixby")
        self._is_bixby = is_bixby

    @property
    def is_discord(self) -> bool:
        return self._is_discord

    @is_discord.setter
    def is_discord(self, is_discord: bool) -> None:
        raise_if_variable_not_expected_type(value=is_discord, expected_type=bool, variable_name="is_discord")
        self._is_discord = is_discord
