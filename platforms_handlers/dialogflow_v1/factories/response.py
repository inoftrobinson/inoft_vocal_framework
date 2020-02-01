from json import dumps as json_dumps

from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from messages import *


class SimpleResponse:
    json_key = "simpleResponse"

    def __init__(self):
        self._textToSpeech = str()
        self._displayText = str()

    @property
    def textToSpeech(self):
        return self._textToSpeech

    @textToSpeech.setter
    def textToSpeech(self, text: str) -> None:
        if isinstance(text, str):
            self._textToSpeech = text
        else:
            raise Exception(f"The text was not a string object : {text}")

    @property
    def displayText(self):
        return self._textToSpeech

    @displayText.setter
    def displayText(self, text: str) -> None:
        if isinstance(text, str):
            self._displayText = text
        else:
            raise Exception(f"The text was not a string object : {text}")

    def to_json_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(
            object_to_process=self, key_names_identifier_objects_to_go_into=["json_key"])


class RichResponseInPayload:
    json_key = "richResponse"

    def __init__(self):
        self._items = list()
        # [{"simpleResponse": { "textToSpeech": f"<speak>{MSGS_FIRST_USE_WELCOME.pick(None)}</speak>", "displayText": "dummy text to display"}}]
        self.suggestions = [
          {
            "title": "Api"
          },
          {
            "title": "Suggestion 2"
          }
        ]

    # "<speak>Here are <say-as interpret-as=\"characters\">SSML</say-as> samples. I can pause <break time=\"3\" />. I can play a sound <audio src=\"https://www.example.com/MY_WAVE_FILE.wav\">your wave file</audio>. I can speak in cardinals. Your position is <say-as interpret-as=\"cardinal\">10</say-as> in line. Or I can speak in ordinals. You are <say-as interpret-as=\"ordinal\">10</say-as> in line. Or I can even speak in digits. Your position in line is <say-as interpret-as=\"digits\">10</say-as>. I can also substitute phrases, like the <sub alias=\"World Wide Web Consortium\">W3C</sub>. Finally, I can speak a paragraph with two sentences. <p><s>This is sentence one.</s><s>This is sentence two.</s></p></speak>"

    @property
    def items(self):
        return self._items

    def add_response_item(self, response_item_object):
        if isinstance(response_item_object, SimpleResponse):
            self._items.insert(0, response_item_object.to_json_dict())
        else:
            raise Exception(f"{type(response_item_object)} is not supported as a response item object type.")

class GoogleInPayload:
    json_key = "google"

    def __init__(self):
        self._expectUserResponse = True
        self.richResponse = RichResponseInPayload()

    @property
    def expectUserResponse(self):
        return self._expectUserResponse

    @expectUserResponse.setter
    def expectUserResponse(self, expectUserResponse) -> None:
        if expectUserResponse is False or expectUserResponse is True:
            self._expectUserResponse = expectUserResponse
        else:
            raise Exception(f"expectUserResponse can only receive a True or False value, it received the following : {expectUserResponse}")

class Payload:
    json_key = "payload"

    def __init__(self):
        self.google = GoogleInPayload()

    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])

if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Payload(), ["json_key"])




