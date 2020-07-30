"""
This file is deprecated and shall not be used. It will soon be discarded in future versions of the framework.
"""


from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.current_used_platform_info import CurrentPlatformData


class Card:
    def __init__(self):
        self._type = None
        self._title = str()
        self._content = str()

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_value) -> None:
        self._type = type_value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title_string: str) -> None:
        self._title = title_string

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content_string: str) -> None:
        self._content = content_string

class OutputSpeech:
    TYPE_KEY_TEXT = "PlainText"
    TYPE_KEY_SSML = "SSML"

    def __init__(self):
        self._type = None
        self._text = str()
        self._ssml = str()

    @property
    def type(self):
        return self._type

    @property
    def text(self):
        return self._text

    @property
    def ssml(self):
        return self._ssml

    def set_text(self, text: str):
        if not isinstance(text, str):
            raise Exception(f"The following text is not a str object : {text}")
        self._type = self.TYPE_KEY_TEXT
        self._text = text
        return self

    def set_ssml(self, ssml_string: str):
        if not isinstance(ssml_string, str):
            raise Exception(f"The following ssml_string is not a str object : {ssml_string}")
        self._type = self.TYPE_KEY_SSML
        self._ssml = ssml_string
        return self

    def set_based_on_type(self, value_to_set: str, type_key: str):
        if type_key == self.TYPE_KEY_SSML:
            self.set_ssml(ssml_string=value_to_set)
        elif type_key == self.TYPE_KEY_TEXT:
            self.set_text(value_to_set)
        else:
            raise Exception(f"Type key {type_key} is not supported.")
        return self

    def get_value_to_use_based_on_set_type(self) -> str:
        if self.type == self.TYPE_KEY_SSML:
            return self.ssml
        elif self.type == self.TYPE_KEY_TEXT:
            return self.text
        else:
            raise Exception(f"The set type_key was not one of the supported type keys.")


class Reprompt:
    def __init__(self):
        self.outputSpeech = OutputSpeech()


class Response:
    def __init__(self):
        self.outputSpeech = OutputSpeech()
        self.reprompt = Reprompt()
        self.card = Card()
        self._shouldEndSession = False

    @property
    def shouldEndSession(self):
        return self._shouldEndSession

    @shouldEndSession.setter
    def shouldEndSession(self, should_end_session: bool) -> None:
        if not isinstance(should_end_session, bool):
            raise Exception(f"should_end_session must be a bool object : {should_end_session}")
        self._shouldEndSession = should_end_session

    def to_platform_dict(self) -> dict:
        from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

        if HandlerInput.is_alexa is True:
            from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.alexa import response
            output_response = response.Response()

            if self.outputSpeech.type == self.outputSpeech.TYPE_KEY_SSML:
                output_response.outputSpeech.set_ssml(self.outputSpeech.ssml)
            elif self.outputSpeech.type == self.outputSpeech.TYPE_KEY_TEXT:
                output_response.outputSpeech.set_text(self.outputSpeech.text)

            output_response.reprompt.outputSpeech.set_text("yaaaazazazaza")

            output_response.shouldEndSession = self.shouldEndSession


            platform_adapted_response_dict = output_response.to_dict()
            print(f"Final platform adapted on Alexa-v1 : {platform_adapted_response_dict}")
            return platform_adapted_response_dict

        elif HandlerInput.is_dialogflow is True:
            from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.dialogflow import response
            output_response = HandlerInput.handler_input.response


            """response_item = response.SimpleResponse()
            response_item.textToSpeech = self.outputSpeech.get_value_to_use_based_on_set_type()
            response_item.displayText = "Yaaaaaazaaaa !!!!!!!"
            output_response.payload.google.richResponse.add_response_item(response_item)"""

            output_response.payload.google.expectUserResponse = True if not self.shouldEndSession else False

            output_response.payload.google.userStorage = str(HandlerInput.persistent_user_data.to_dict())

            session_user_data_context_item = response.OutputContextItem()
            for key_item_saved_data, value_item_saved_data in HandlerInput.session_user_data.to_dict().items():
                session_user_data_context_item.add_set_session_attribute(key_item_saved_data, value_item_saved_data)
            output_response.add_output_context_item(session_user_data_context_item)

            platform_adapted_response_dict = output_response.to_dict()
            print(f"Final platform adapted on Google-Assistant-v1 : {platform_adapted_response_dict}")
            return platform_adapted_response_dict
        else:
            raise Exception(f"Platform with id {CurrentPlatformData.used_platform_id} is not supported.")
