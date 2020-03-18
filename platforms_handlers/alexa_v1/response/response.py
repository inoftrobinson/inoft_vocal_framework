from collections import Callable

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_value_not_in_list
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.utils.general import is_text_ssml


class Image:
    json_key = "image"

    def __init__(self, small_image_url: str, large_image_url: str):
        self._smallImageUrl = small_image_url
        self._largeImageUrl = large_image_url

    @property
    def smallImageUrl(self) -> str:
        return self._smallImageUrl

    @smallImageUrl.setter
    def smallImageUrl(self, smallImageUrl: str) -> None:
        if not isinstance(smallImageUrl, str):
            raise Exception(f"smallImageUrl was type {type(smallImageUrl)} which is not valid value for his parameter.")
        self._smallImageUrl = smallImageUrl

    @property
    def largeImageUrl(self) -> str:
        return self._largeImageUrl

    @largeImageUrl.setter
    def largeImageUrl(self, largeImageUrl: str) -> None:
        if not isinstance(largeImageUrl, str):
            raise Exception(f"largeImageUrl was type {type(largeImageUrl)} which is not valid value for his parameter.")
        self._largeImageUrl = largeImageUrl

class Card:
    json_key = "card"

    type_simple = "Simple"
    type_standard = "Standard"
    type_link_account = "LinkAccount"
    type_ask_for_permissions_content = "AskForPermissionsConsent"
    available_types = [type_simple, type_standard, type_link_account, type_ask_for_permissions_content]

    def __init__(self, type_value: str, title: str, text: str = None, content_text: str = None, image: Image = None):
        self._type = type_value
        self._title = title
        self._text = text
        self._content = content_text
        self._image = image

    def do_not_include(self):
        if (self._type is None) or (self._title == "" and self._content == ""):
            return True
        else:
            return False

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type_value: str) -> None:
        if type_value not in self.available_types:
            raise Exception(f"The type_value {type_value} is not a supported type in {self.available_types}")
        self._type = type_value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        self._title = title

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if not isinstance(text, str):
            raise Exception(f"text was type {type(text)} which is not valid value for his parameter.")
        self._text = text

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content: str) -> None:
        self._content = content

    @property
    def image(self) -> Image:
        if self._image is None:
            self._image = Image()
        return self._image

class Directives(list):
    json_key = "directives"

    def __init__(self):
        super().__init__()

    class AudioPlayer:
        json_key = None
        TYPE_PLAY = "AudioPlayer.Play"
        AVAILABLE_TYPES = [TYPE_PLAY]
        PLAY_BEHAVIOR_REPLACE_ALL = "REPLACE_ALL"
        AVAILABLE_PLAY_BEHAVIORS = [PLAY_BEHAVIOR_REPLACE_ALL]
        # todo: include a warning when using an audio played if the skill do not has the
        #  audio player setting activated (i lost like 20 minutes on this dumb thing)

        class AudioItem:
            json_key = "audioItem"

            class Stream:
                json_key = "stream"

                def __init__(self, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
                    self.token = token_identifier
                    self.url = url
                    self.offsetInMilliseconds = offsetInMilliseconds

                @property
                def token(self) -> str:
                    return self._token

                @token.setter
                def token(self, token: str) -> None:
                    raise_if_variable_not_expected_type(value=token, expected_type=str, variable_name="token")
                    self._token = token

                @property
                def url(self) -> str:
                    return self._url

                @url.setter
                def url(self, url: str) -> None:
                    raise_if_variable_not_expected_type(value=url, expected_type=str, variable_name="url")
                    self._url = url

                @property
                def offsetInMilliseconds(self) -> int:
                    return self._offsetInMilliseconds

                @offsetInMilliseconds.setter
                def offsetInMilliseconds(self, offsetInMilliseconds: int) -> None:
                    raise_if_variable_not_expected_type(value=offsetInMilliseconds, expected_type=int, variable_name="offsetInMilliseconds")
                    self._offsetInMilliseconds = offsetInMilliseconds

            def __init__(self, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
                self._stream = self.Stream(token_identifier=token_identifier, url=url, offsetInMilliseconds=offsetInMilliseconds)

            @property
            def stream(self) -> Stream:
                return self._stream

        def __init__(self, played_type: str, play_behavior: str, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
            self.type = played_type
            self._playBehavior = play_behavior
            self._audioItem = self.AudioItem(token_identifier=token_identifier, url=url, offsetInMilliseconds=offsetInMilliseconds)

        @property
        def type(self) -> str:
            return self._type

        @type.setter
        def type(self, type_value: str) -> None:
            raise_if_value_not_in_list(value=type_value, list_object=self.AVAILABLE_TYPES, variable_name="type")
            self._type = type_value

        @property
        def playBehavior(self) -> str:
            return self._playBehavior

        @playBehavior.setter
        def playBehavior(self, playBehavior: str) -> None:
            raise_if_value_not_in_list(value=playBehavior, list_object=self.AVAILABLE_PLAY_BEHAVIORS, variable_name="playBehavior")
            self._playBehavior = playBehavior

        @property
        def audioItem(self) -> AudioItem:
            return self._audioItem

    @property
    def audioPlayer(self) -> AudioPlayer:
        for directive in self:
            if isinstance(directive, self.AudioPlayer):
                return directive

    def add_audio_player(self, played_type: str, play_behavior: str, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
        if self.audioPlayer is not None:
            raise Exception(f"AudioPlayer has already been set and cannot be set twice")
        self.append(self.AudioPlayer(played_type=played_type, play_behavior=play_behavior,
                                     token_identifier=token_identifier, url=url,
                                     offsetInMilliseconds=offsetInMilliseconds))

    def do_not_include(self) -> bool:
        return True if len(self) == 0 else False


class OutputSpeech:
    TYPE_KEY_TEXT = "PlainText"
    TYPE_KEY_SSML = "SSML"
    json_key = "outputSpeech"

    def __init__(self):
        self._type = None
        self._text = None
        self._ssml = None

    def is_speech_empty(self):
        if self._type == self.TYPE_KEY_TEXT:
            return True if self.text is None else False
        elif self._type == self.TYPE_KEY_SSML:
            return True if self.ssml is None else False
        else:
            return True

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        raise_if_variable_not_expected_type(value=text, expected_type=str, variable_name="text")
        self._type = "PlainText"
        self._text = text

    @property
    def ssml(self):
        return self._ssml

    @ssml.setter
    def ssml(self, ssml: str) -> None:
        raise_if_variable_not_expected_type(value=ssml, expected_type=str, variable_name="ssml")
        self._type = "SSML"
        self._ssml = ssml

    def set_based_on_type(self, value_to_set: str, type_key: str):
        if type_key == self.TYPE_KEY_SSML:
            self.ssml = value_to_set
        elif type_key == self.TYPE_KEY_TEXT:
            self.text = value_to_set
        else:
            raise Exception(f"Type key {type_key} is not supported.")
        return self

    def do_not_include(self):
        return self.is_speech_empty()

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
        self._directives = Directives()
        self._card = None
        self._shouldEndSession = False

    def say(self, text_or_ssml: str):
        if is_text_ssml(text_or_ssml=text_or_ssml) is True:
            self.outputSpeech.ssml = text_or_ssml
        else:
            self.outputSpeech.text = text_or_ssml

    def say_reprompt(self, text_or_ssml: str):
        if is_text_ssml(text_or_ssml=text_or_ssml) is True:
            self.reprompt.outputSpeech.ssml = text_or_ssml
        else:
            self.reprompt.outputSpeech.text = text_or_ssml

    def play_audio(self, identifier: str,  mp3_file_url: str,
                   title: str, subtitle: str, icon_image_url: str, background_image_url: str,
                   milliseconds_start_offset: int = 0,
                   played_type: str = Directives.AudioPlayer.TYPE_PLAY,
                   play_behavior: str = Directives.AudioPlayer.PLAY_BEHAVIOR_REPLACE_ALL,
                   override_default_end_session: bool = False):

        # todo: check mp3 file validity
        self.directives.add_audio_player(played_type=played_type, play_behavior=play_behavior,
                                         token_identifier=identifier, url=mp3_file_url,
                                         offsetInMilliseconds=milliseconds_start_offset)

        if override_default_end_session is False:
            self.end_session()
        # When playing an audio file, by default we end the session so that the file will be played (it can be overridden with an argument)

    def end_session(self, should_end: bool = True):
        self.shouldEndSession = should_end

    @property
    def outputSpeech(self) -> OutputSpeech:
        return self._outputSpeech

    @property
    def reprompt(self) -> Reprompt:
        return self._reprompt

    @property
    def directives(self) -> Directives:
        return self._directives

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card: Card) -> None:
        raise_if_variable_not_expected_type(value=card, expected_type=Card, variable_name="card")
        self._card = card

    @property
    def shouldEndSession(self):
        return self._shouldEndSession

    @shouldEndSession.setter
    def shouldEndSession(self, shouldEndSession: bool) -> None:
        raise_if_variable_not_expected_type(value=shouldEndSession, expected_type=bool, variable_name="shouldEndSession")
        self._shouldEndSession = shouldEndSession

    def to_dict(self) -> dict:
        dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                                     key_names_identifier_objects_to_go_into=["json_key"])
        dict_object["version"] = "1.0"
        dict_object["sessionAttributes"] = dict()
        return dict_object

if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Response(), ["json_key"])
