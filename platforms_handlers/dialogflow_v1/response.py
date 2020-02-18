from json import dumps as json_dumps

from inoft_vocal_framework.platforms_handlers.current_platform_static_data import SessionInfo
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
        self._userStorage = str()

    @property
    def expectUserResponse(self):
        return self._expectUserResponse

    @expectUserResponse.setter
    def expectUserResponse(self, expectUserResponse) -> None:
        if expectUserResponse is False or expectUserResponse is True:
            self._expectUserResponse = expectUserResponse
        else:
            raise Exception(f"expectUserResponse can only receive a True or False value, it received the following : {expectUserResponse}")

    @property
    def userStorage(self) -> str:
        return self._userStorage

    @userStorage.setter
    def userStorage(self, userStorage: str) -> None:
        if not isinstance(userStorage, str):
            raise Exception(f"userStorage was type {type(userStorage)} which is not valid value for his parameter.")
        self._userStorage = userStorage

class Payload:
    json_key = "payload"

    def __init__(self):
        self.google = GoogleInPayload()

    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])

class OutputContextItem:
    json_key = "outputContextItem"

    def __init__(self):
        self.name = f"{SessionInfo.session_id}/contexts/test"
        self.lifespanCount = int()
        self._parameters = dict()

    def return_transformations(self) -> None:
        self._parameters = self._parameters  # json.dumps()

    def add_set_parameter(self, parameter_key: str, parameter_value=None):
        """
        :param parameter_key: str key for the parameters dict object, should not be an empty str
        :param parameter_value: any object, cannot be None
        :return: self
        """
        if parameter_value is not None and isinstance(parameter_key, str) and parameter_key != "":
            self._parameters[parameter_key] = parameter_value
        return self

    def add_set_session_attribute(self, parameter_key: str, parameter_value=None):
        if "data" not in self.parameters.keys():
            self.parameters["data"] = dict()

        if parameter_value is not None and isinstance(parameter_key, str) and parameter_key != "":
            self._parameters["data"][parameter_key] = parameter_value
        return self

    @property
    def parameters(self) -> dict:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: dict) -> None:
        if not isinstance(parameters, dict):
            raise Exception(f"parameters was type {type(parameters)} which is not valid value for his parameter.")
        self._parameters = parameters

class Response:
    json_key = "response"

    def __init__(self):
        self.payload = Payload()
        self.outputContexts = list()

    def say(self, text_or_ssml: str) -> None:
        # todo: allow to have 2 differents response in the same one, not just one
        output_response = SimpleResponse()
        output_response.textToSpeech = text_or_ssml
        self.payload.google.richResponse.add_response_item(output_response)

    def reprompt(self, text_or_ssml: str) -> None:
        # todo: finish the reprompt function
        return None
        output_response = SimpleResponse()
        output_response.textToSpeech = text_or_ssml
        self.payload.google.richResponse.add_response_item(output_response)

    def add_output_context_item(self, output_context_item: OutputContextItem) -> None:
        if isinstance(output_context_item, OutputContextItem):
            self.outputContexts.append(output_context_item)
        else:
            raise Exception(f"The output context item needed to be of instance {OutputContextItem} but was : {output_context_item}")

    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])[self.json_key]


if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Payload(), ["json_key"])




