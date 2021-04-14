from typing import Optional

from pydantic import Field
from pydantic.main import BaseModel

from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.utils.general import is_text_ssml


class Image(BaseModel):
    smallImageUrl: Optional[str] = None
    largeImageUrl: Optional[str] = None


class Card(BaseModel):
    type_simple = "Simple"
    type_standard = "Standard"
    type_link_account = "LinkAccount"
    type_ask_for_permissions_content = "AskForPermissionsConsent"
    available_types = [type_simple, type_standard, type_link_account, type_ask_for_permissions_content]

    type: str
    title: str
    text: str
    content: Optional[str] = None
    image: Optional[Image] = None

    # def __init__(self, type_value: str, title: str, text: str = None, content_text: str = None, image: Image = None):

    def do_not_include(self):
        if (self.type is None) or (self.title == "" and self.content == ""):
            return True
        else:
            return False

    @property
    def image(self) -> Image:
        if self._image is None:
            self._image = Image()
        return self._image

class Directives(list):
    @property
    def audioPlayer(self):
        from inoft_vocal_framework.platforms_handlers.alexa.audioplayer import AudioPlayer
        for directive in self:
            if isinstance(directive, AudioPlayer):
                return directive

    def add_audio_player(self, played_type: str, play_behavior: str, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
        if self.audioPlayer is not None:
            raise Exception(f"AudioPlayer has already been set and cannot be set twice")

        from inoft_vocal_framework.platforms_handlers.alexa.audioplayer import AudioPlayer
        self.append(AudioPlayer(played_type=played_type, play_behavior=play_behavior,
                                token_identifier=token_identifier, url=url,
                                offsetInMilliseconds=offsetInMilliseconds))

    def do_not_include(self) -> bool:
        return True if len(self) == 0 else False


class OutputSpeech(BaseModel):
    _TYPE_KEY_TEXT = "PlainText"
    _TYPE_KEY_SSML = "SSML"

    type: Optional[str] = None
    text: Optional[str] = None
    ssml: Optional[str] = None

    def is_speech_empty(self):
        if self._type == self._TYPE_KEY_TEXT:
            return True if self.text is None else False
        elif self._type == self._TYPE_KEY_SSML:
            return True if self.ssml is None else False
        else:
            return True

    def reset(self):
        self.text = None
        self.ssml = None

    def set_based_on_type(self, value_to_set: str, type_key: str):
        if type_key == self._TYPE_KEY_SSML:
            self.ssml = value_to_set
        elif type_key == self._TYPE_KEY_TEXT:
            self.text = value_to_set
        else:
            raise Exception(f"Type key {type_key} is not supported.")
        return self

    def do_not_include(self):
        return self.is_speech_empty()

    def return_transformations(self):
        if self.ssml is not None and not is_text_ssml(self.ssml):
            self.ssml = f"<speak>{self.ssml}</speak>"

class Reprompt(BaseModel):
    outputSpeech: OutputSpeech = Field(default_factory=OutputSpeech)

    def do_not_include(self):
        # todo: implement do_not_include with Pydantic
        return self.outputSpeech.is_speech_empty()

class Response(BaseModel):
    outputSpeech: OutputSpeech = Field(default_factory=OutputSpeech)
    reprompt: Reprompt = Field(default_factory=Reprompt)
    directives: Directives = Field(default_factory=Directives)
    card: Optional[Card] = None
    shouldEndSession: bool = False

    def say(self, text_or_ssml: str):
        if is_text_ssml(text_or_ssml=text_or_ssml) is True:
            self.say_ssml(ssml=text_or_ssml)
        else:
            self.outputSpeech.text = f'{self.outputSpeech.text}\n{text_or_ssml}' if self.outputSpeech.text is not None else text_or_ssml

    def say_ssml(self, ssml: str):
        self.outputSpeech.ssml = f'{self.outputSpeech.ssml}\n{ssml}' if self.outputSpeech.ssml is not None else ssml

    def clear_speech(self):
        self.outputSpeech.reset()

    def say_reprompt(self, text_or_ssml: str):
        if is_text_ssml(text_or_ssml=text_or_ssml) is True:
            self.reprompt.outputSpeech.ssml = f'{self.reprompt.outputSpeech.ssml}\n{text_or_ssml}' if self.reprompt.outputSpeech.ssml is not None else text_or_ssml
        else:
            self.reprompt.outputSpeech.text = f'{self.reprompt.outputSpeech.text}\n{text_or_ssml}' if self.reprompt.outputSpeech.text is not None else text_or_ssml

    def clear_reprompt_speech(self):
        self.reprompt.outputSpeech.reset()

    @property
    def audioplayer(self):
        from inoft_vocal_framework.platforms_handlers.alexa.audioplayer import AudioPlayer
        for directive in self.directives:
            if isinstance(directive, AudioPlayer):
                return directive

    # todo: to remove its deprecated (use the audioplayer object)
    def play_audio(
            self, identifier: str,  mp3_file_url: str,
            title: str, subtitle: str, icon_image_url: str, background_image_url: str,
            milliseconds_start_offset: int = 0, played_type: str = None, play_behavior: str = None,
            override_default_end_session: bool = False
    ):

        from inoft_vocal_framework.platforms_handlers.alexa.audioplayer import AudioPlayer
        if played_type is None:
            played_type = AudioPlayer.TYPE_PLAY
        if play_behavior is None:
            play_behavior = AudioPlayer.PLAY_BEHAVIOR_REPLACE_ALL

        # todo: check mp3 file validity
        self.directives.add_audio_player(
            played_type=played_type, play_behavior=play_behavior,
            token_identifier=identifier, url=mp3_file_url,
            offsetInMilliseconds=milliseconds_start_offset
        )

        if override_default_end_session is False:
            self.end_session()
        # When playing an audio file, by default we end the session so that the file will be played (it can be overridden with an argument)

    def end_session(self, should_end: bool = True):
        self.shouldEndSession = should_end

    def to_dict(self) -> dict:
        dict_object = self.dict()
        dict_object['version'] = "1.0"
        dict_object['sessionAttributes'] = dict()
        return dict_object

if __name__ == "__main__":
    NestedObjectToDict.get_dict_from_nested_object(Response(), ["json_key"])
