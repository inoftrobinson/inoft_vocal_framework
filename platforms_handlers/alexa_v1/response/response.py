from json import dumps as json_dumps
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.utils.general import is_text_ssml
from messages import *

class Card:
    json_key = "card"

    def __init__(self):
        self._type = None
        self._title = str()
        self._content = str()

    def do_not_include(self):
        if (self._type is None) or (self._title == "" and self._content == ""):
            return True
        else:
            return False

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
    json_key = "outputSpeech"

    def __init__(self):
        self._type = None
        self._text = str()
        self._ssml = str()

    def is_speech_empty(self):
        if self._type == self.TYPE_KEY_TEXT:
            return True if self._text.replace(" ", "") == "" else False
        elif self._type == self.TYPE_KEY_SSML:
            return True if self._text.replace(" ", "") == "" else False
        else:
            return True

    def set_text(self, text: str):
        if not isinstance(text, str):
            raise Exception(f"The following text is not a str object : {text}")
        self._type = "PlainText"
        self._text = text
        return self

    def set_ssml(self, ssml_string: str):
        if not isinstance(ssml_string, str):
            raise Exception(f"The following ssml_string is not a str object : {ssml_string}")
        self._type = "SSML"
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

class Reprompt:
    json_key = "reprompt"

    def __init__(self):
        self.outputSpeech = OutputSpeech()

    def do_not_include(self):
        return self.outputSpeech.is_speech_empty()

class Response:
    json_key = "response"

    def __init__(self):
        self._outputSpeech = OutputSpeech()
        self._reprompt = Reprompt()
        self._card = Card()
        self._shouldEndSession = False

    def say(self, text_or_ssml: str):
        is_ssml = is_text_ssml(text_or_ssml=text_or_ssml)

        if is_ssml is True:
            self.outputSpeech.set_ssml(ssml_string=text_or_ssml)
        else:
            self.outputSpeech.set_text(text=text_or_ssml)

    def reprompt(self, text_or_ssml: str):
        is_ssml = is_text_ssml(text_or_ssml=text_or_ssml)

        if is_ssml is True:
            self._reprompt.outputSpeech.set_ssml(ssml_string=text_or_ssml)
        else:
            self._reprompt.outputSpeech.set_text(text=text_or_ssml)

    @property
    def outputSpeech(self) -> OutputSpeech:
        return self._outputSpeech

    @property
    def card(self) -> Card:
        return self._card

    @property
    def shouldEndSession(self):
        return self._shouldEndSession

    @shouldEndSession.setter
    def shouldEndSession(self, should_end_session: bool) -> None:
        if not isinstance(should_end_session, bool):
            raise Exception(f"should_end_session must be a bool object : {should_end_session}")
        self._shouldEndSession = should_end_session

    def to_dict(self) -> dict:
        dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                                     key_names_identifier_objects_to_go_into=["json_key"])
        dict_object["version"] = "1.0"
        dict_object["sessionAttributes"] = dict()
        return dict_object

if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Response(), ["json_key"])
