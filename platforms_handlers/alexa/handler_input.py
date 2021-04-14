from typing import Optional, Union

from pydantic import PrivateAttr
from pydantic.main import BaseModel

from inoft_vocal_framework.platforms_handlers.alexa.audioplayer.audioplayer_directives import AudioPlayerWrapper
from inoft_vocal_framework.platforms_handlers.alexa.context import Context
from inoft_vocal_framework.platforms_handlers.alexa.request import Request
from inoft_vocal_framework.platforms_handlers.alexa.response.response import Response
from inoft_vocal_framework.platforms_handlers.alexa.session import Session
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


class AlexaHandlerInput(BaseModel):
    from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

    session: Session
    context: Context
    request: Request

    _response: Response = PrivateAttr(default_factory=Response)
    _parent_handler_input: HandlerInput = PrivateAttr()
    _is_new_session: Optional[bool] = PrivateAttr(default=None)
    _session_attributes: Optional[dict] = PrivateAttr(default=None)
    _audio_player: Optional[AudioPlayerWrapper] = PrivateAttr(default=None)

    def __init__(self, parent_handler_input: HandlerInput, **kwargs):
        super().__init__(**kwargs)
        self._parent_handler_input = parent_handler_input

    @property
    def is_new_session(self) -> bool:
        if self._is_new_session is None:
            self._is_new_session = self.session.new if isinstance(self.session.new, bool) else False
        return self._is_new_session

    def is_launch_request(self) -> bool:
        return self.request.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        return self.request.is_in_intent_names(intent_names_list=intent_names_list)

    def is_in_request_types(self, request_types_list: list):
        return self.request.is_in_request_types(request_types_list=request_types_list)

    # todo: create a new function that handle the end of a session (like an optionnal function in each class type ?)
    def say(self, text_or_ssml: str) -> None:
        self._response.say(text_or_ssml=text_or_ssml)

    def say_ssml(self, ssml: str) -> None:
        self._response.say_ssml(ssml=ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        # todo: fix reprompt (for alexa and dialogflow)
        self._response.say_reprompt(text_or_ssml=text_or_ssml)

    def play_audio_block(self, audio_block: AudioBlock, num_channels: 1 or 2 = 1, sample_rate: 24000 or 22050 or 16000 = 24000) -> bool:
        file_url = audio_block.manual_render(
            num_channels=num_channels, sample_rate=sample_rate, bitrate=48,
            out_filepath="null", format_type="mp3"
        )
        # todo: make out_filepath argument optional
        self.say_ssml(f'<audio src="{file_url}" />')
        return True  # todo: return False is rendering failed

    @property
    def audioplayer(self) -> AudioPlayerWrapper:
        if self._audioplayer is None:
            self._audioplayer = AudioPlayerWrapper(parent_handler_input=self._parent_handler_input)
        return self._audioplayer

    def save_audioplayer_handlers_group_class(self, handlers_group_class_type: type, group_class_kwargs: dict = None):
        from inspect import getfile
        # We use the persistent attributes and not the session, because after launching an audio file with the audio player,
        # the session of the user will end. Then when interacting with an audio file there will be no session id.
        # So, if we save this data as session attributes, it would be considered of the same session only if the smart
        # session timeout has not been exceeded. Which is not at all what we want.
        self._parent_handler_input.persistent_memorize(
            data_key='lastUsedAudioPlayerHandlersGroupClass',
            data_value={
                "fileFilepathContainingClass": getfile(handlers_group_class_type),
                "classPath": handlers_group_class_type.__qualname__,
                "classKwargs": group_class_kwargs
            }
        )

    def get_last_used_audioplayer_handlers_group(self) -> SafeDict:
        return SafeDict(self._parent_handler_input.persistent_remember('lastUsedAudioPlayerHandlersGroupClass', specific_object_type=dict))

    def show_basic_card(self, title: str, text: str, small_image_url: Optional[str] = None, large_image_url: Optional[str] = None) -> None:
        from inoft_vocal_framework.platforms_handlers.alexa.response import Card
        if small_image_url is not None or large_image_url is not None:
            from inoft_vocal_framework.platforms_handlers.alexa.response import Image

            if small_image_url is None and large_image_url is not None:
                small_image_url = large_image_url
                print("WARNING ! The small_image_url argument was not specified, the large_image_url"
                      "argument (which has been specified) is now also used as the small_image_url.")
            elif large_image_url is None and small_image_url is not None:
                large_image_url = small_image_url
                print("WARNING ! The large_image_url argument was not specified, the small_image_url"
                      "argument (which has been specified) is now also used as the large_image_url.")

            self._response.card = Card(
                type_value=Card.type_standard, title=title, text=text,
                image=Image(small_image_url=small_image_url, large_image_url=large_image_url)
            )
        else:
            self._response.card = Card(type_value=Card.type_simple, title=title, content_text=text)

    def show_link_account_card(self) -> None:
        raise Exception("Not yet implemented")

    def show_ask_permissions_card(self) -> None:
        raise Exception("Not yet implemented")

    def end_session(self, should_end: bool = True) -> None:
        self._response.end_session(should_end=should_end)

    @property
    def session_attributes(self) -> dict:
        if self._session_attributes is None:
            self._session_attributes = self.session.attributes if isinstance(self.session.attributes, dict) else {}
        return self._session_attributes

