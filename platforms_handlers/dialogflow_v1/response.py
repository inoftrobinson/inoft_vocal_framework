from json import dumps as json_dumps
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict


class Image:
    json_key = "image"

    def __init__(self):
        self._url = str()
        self._accessibilityText = str()


class ImageDisplayOptions:
    json_key = "imageDisplayOptions"

    cropped_type = "CROPPED"
    available_options_types = [cropped_type]

    def __init__(self):
        self._option_type = str()

    @property
    def option_type(self) -> str:
        return self._option_type

    @option_type.setter
    def option_type(self, option_type: str) -> None:
        if not isinstance(option_type, str):
            raise Exception(f"option_type was type {type(option_type)} which is not valid value for his parameter.")
        if option_type not in self.available_options_types:
            raise Exception(f"The option_type {option_type} was not a valid display options type.")
        self._option_type = option_type

class Button:
    def __init__(self):
        self._title = str()
        self._openUrlAction = str()

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        if not isinstance(title, str):
            raise Exception(f"title was type {type(title)} which is not valid value for his parameter.")
        self._title = title

    @property
    def openUrlAction(self) -> str:
        return self._openUrlAction

    @openUrlAction.setter
    def openUrlAction(self, openUrlAction: str) -> None:
        if not isinstance(openUrlAction, str):
            raise Exception(f"openUrlAction was type {type(openUrlAction)} which is not valid value for his parameter.")
        self._openUrlAction = openUrlAction

class BasicCard:
    json_key = "basicCard"

    def __init__(self, title: str, subtitle: str, formatted_text: str = None, buttons: list = None,
                 image: Image = None, image_display_options: ImageDisplayOptions = None):

        self._title = title
        self._subtitle = subtitle
        self._formattedText = formatted_text
        self._buttons = buttons
        self._image = image
        self._imageDisplayOptions = image_display_options

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        if not isinstance(title, str):
            raise Exception(f"title was type {type(title)} which is not valid value for his parameter.")
        self._title = title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str) -> None:
        if not isinstance(subtitle, str):
            raise Exception(f"subtitle was type {type(subtitle)} which is not valid value for his parameter.")
        self._subtitle = subtitle

    @property
    def formattedText(self) -> str:
        return self._formattedText

    @formattedText.setter
    def formattedText(self, formattedText: str) -> None:
        if not isinstance(formattedText, str):
            raise Exception(f"formattedText was type {type(formattedText)} which is not valid value for his parameter.")
        self._formattedText = formattedText

    @property
    def buttons(self) -> list:
        return self._buttons

    @buttons.setter
    def buttons(self, buttons: list) -> None:
        if not isinstance(buttons, list):
            raise Exception(f"buttons was type {type(buttons)} which is not valid value for his parameter.")
        self._buttons = buttons

    @property
    def image(self) -> Image:
        return self._image

    @image.setter
    def image(self, image: Image) -> None:
        if not isinstance(image, Image):
            raise Exception(f"image was type {type(image)} which is not valid value for his parameter.")
        self._image = image

    @property
    def imageDisplayOptions(self):
        return self._imageDisplayOptions

    @imageDisplayOptions.setter
    def imageDisplayOptions(self, imageDisplayOptionType: str) -> None:
        if not isinstance(imageDisplayOptionType, str):
            raise Exception(f"imageDisplayOptionType was type {type(imageDisplayOptionType)} which is not valid value for his parameter.")
        self._imageDisplayOptions.option_type = imageDisplayOptionType

    def return_transformations(self) -> None:
        self._imageDisplayOptions = self._imageDisplayOptions if self._imageDisplayOptions is None else self._imageDisplayOptions.option_type()


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
        self.suggestions = list()

    @property
    def items(self):
        return self._items

    def add_response_item(self, response_item_object):
        response_item_dict = NestedObjectToDict.get_dict_from_nested_object(
            object_to_process=response_item_object, key_names_identifier_objects_to_go_into=["json_key"])
        self._items.append(response_item_dict)

    def add_suggestion_chip(self, title: str):
        # todo: add external link suggestion chip (cannot be used on platforms without the actions.capability.WEB_BROWSER capability
        if not isinstance(title, str):
            raise Exception(f"The title variable must be of type str but was {type(title)}")
        if len(title) > 25:
            raise Exception(f"A suggestion chip title can have a maximum of 25 chars but {title} was {len(title)} chars")

        self.suggestions.append({"title": title})

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
    session_data_name = "sessionData"

    def __init__(self, session_id: str, name:str, lifespanCount=999):
        self.name = f"{session_id}/contexts/{name}"
        self.lifespanCount = lifespanCount
        self._parameters = dict()

    def return_transformations(self) -> None:
        if "data" in self.parameters.keys():
            self.parameters["data"] = json_dumps(self._parameters["data"])

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

    def add_response_item_to_show(self, item_object) -> None:
        if not len(self.payload.google.richResponse.items) > 0:
            raise Exception("A google response take in consideration the order with which the elements have been added. "
                            "You cannot set a visual element as first element of the response. "
                            "Try to set a speech element with the .say() function before you add a visual element.")
        self.payload.google.richResponse.add_response_item(item_object)

    def add_suggestions_chips(self, chips_titles: list) -> None:
        if isinstance(chips_titles, list):
            for chip_title in chips_titles:
                self.payload.google.richResponse.add_suggestion_chip(title=chip_title)
        elif isinstance(chips_titles, str):
            self.payload.google.richResponse.add_suggestion_chip(title=chips_titles)

    def to_dict(self) -> dict:
        return NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                              key_names_identifier_objects_to_go_into=["json_key"])[self.json_key]


if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Payload(), ["json_key"])




