import logging

from inoft_vocal_framework.dummy_object import DummyObject
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_value_not_in_list, raise_if_variable_not_expected_type_and_not_none
from inoft_vocal_framework.safe_dict import SafeDict


# todo: refactor to Pydantic

class AudioPlayer:
    json_key = None
    TYPE_PLAY = "AudioPlayer.Play"
    TYPE_STOP = "AudioPlayer.Stop"
    TYPE_CLEAR_QUEUE = "AudioPlayer.ClearQueue"
    AVAILABLE_TYPES = [TYPE_PLAY, TYPE_STOP, TYPE_CLEAR_QUEUE]
    PLAY_BEHAVIOR_REPLACE_ALL = "REPLACE_ALL"
    AVAILABLE_PLAY_BEHAVIORS = [PLAY_BEHAVIOR_REPLACE_ALL]
    CLEAR_BEHAVIOR_CLEAR_QUEUE = "CLEAR_ENQUEUED"
    CLEAR_BEHAVIOR_CLEAR_ALL = "CLEAR_ALL"
    AVAILABLE_CLEAR_BEHAVIORS = [CLEAR_BEHAVIOR_CLEAR_QUEUE, CLEAR_BEHAVIOR_CLEAR_ALL]

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
                raise_if_variable_not_expected_type(value=offsetInMilliseconds, expected_type=int,
                                                    variable_name="offsetInMilliseconds")
                self._offsetInMilliseconds = offsetInMilliseconds

        def __init__(self, token_identifier: str, url: str, offsetInMilliseconds: int = 0):
            self.stream = self.Stream(token_identifier=token_identifier, url=url,
                                      offsetInMilliseconds=offsetInMilliseconds)

    def __init__(self, played_type: str, play_behavior: str = None, clear_behavior: str = None,
                 token_identifier: str = None, url: str = None, offsetInMilliseconds: int = 0):
        self.type = played_type
        self._playBehavior = play_behavior
        self._clearBehavior = clear_behavior

        if token_identifier is not None and url is not None:
            self.audioItem = self.AudioItem(token_identifier=token_identifier, url=url,
                                            offsetInMilliseconds=offsetInMilliseconds)

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
    def clearBehavior(self) -> str:
        return self._clearBehavior

    @clearBehavior.setter
    def clearBehavior(self, clearBehavior: str) -> None:
        raise_if_value_not_in_list(value=clearBehavior, list_object=self.AVAILABLE_CLEAR_BEHAVIORS, variable_name="clearBehavior")
        self._clearBehavior = clearBehavior


class AudioItemObject(object):
    # This object is not used for parsing, but for data manipulation
    def __init__(self, identifier: str, audio_item_dict: dict = None):
        self.identifier = identifier

        if audio_item_dict is not None:
            if isinstance(audio_item_dict, dict):
                audio_item_dict = SafeDict(audio_item_dict)
            if not isinstance(audio_item_dict, SafeDict):
                raise Exception(f"The audio_item_dict must be of type dict or SafeDict but was {type(audio_item_dict)}: {audio_item_dict}")

            self.mp3_file_url = audio_item_dict.get("url").to_str()
            self.title = audio_item_dict.get("title").to_str()
            self.subtitle = audio_item_dict.get("subtitle").to_str()
            self.offset_in_milliseconds = audio_item_dict.get("offsetInMilliseconds").to_int()
            self.icon_image_url = audio_item_dict.get("iconImageUrl").to_str()
            self.background_image_url = audio_item_dict.get("backgroundImageUrl").to_str()

    def to_dict(self):
        return {
            "identifier": self.identifier,
            "url": self.mp3_file_url,
            "title": self.title,
            "subtitle": self.subtitle,
            "offsetInMilliseconds": self.offset_in_milliseconds,
            "iconImageUrl": self.icon_image_url,
            "backgroundImageUrl": self.background_image_url,
        }

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        raise_if_variable_not_expected_type(value=identifier, expected_type=str, variable_name="identifier")
        self._identifier = identifier

    @property
    def mp3_file_url(self) -> str:
        return self._mp3_file_url

    @mp3_file_url.setter
    def mp3_file_url(self, mp3_file_url: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=mp3_file_url, expected_type=str, variable_name="mp3_file_url")
        self._mp3_file_url = mp3_file_url

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=title, expected_type=str, variable_name="title")
        self._title = title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @subtitle.setter
    def subtitle(self, subtitle: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=subtitle, expected_type=str, variable_name="subtitle")
        self._subtitle = subtitle

    @property
    def offset_in_milliseconds(self) -> int:
        return self._offset_in_milliseconds

    @offset_in_milliseconds.setter
    def offset_in_milliseconds(self, offset_in_milliseconds: int) -> None:
        if isinstance(offset_in_milliseconds, str) and offset_in_milliseconds.isdigit():
            offset_in_milliseconds = int(offset_in_milliseconds)
        raise_if_variable_not_expected_type_and_not_none(value=offset_in_milliseconds, expected_type=int, variable_name="offset_in_milliseconds")
        self._offset_in_milliseconds = offset_in_milliseconds

    @property
    def icon_image_url(self) -> str:
        return self._icon_image_url

    @icon_image_url.setter
    def icon_image_url(self, icon_image_url: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=icon_image_url, expected_type=str, variable_name="icon_image_url")
        self._icon_image_url = icon_image_url

    @property
    def background_image_url(self) -> str:
        return self._background_image_url

    @background_image_url.setter
    def background_image_url(self, background_image_url: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=background_image_url, expected_type=str, variable_name="background_image_url")
        self._background_image_url = background_image_url

class AudioPlayerWrapper:
    def __init__(self, parent_handler_input):
        self.parent_handler_input = parent_handler_input
        self._audioPlayer = None

        self._history = None

    @property
    def audioPlayer(self):
        if self._audioPlayer is None:
            return DummyObject()
        return self._audioPlayer

    @audioPlayer.setter
    def audioPlayer(self, audioPlayer: AudioPlayer) -> None:
        if self._audioPlayer is not None:
            logging.warning(f"The AudioPlayer has been with a playBehavior of {audioPlayer.playBehavior} where it had already"
                            f"been set to another AudioPlayer with a playBehavior of {self._audioPlayer.playBehavior}."
                            f"Normally you should set the AudioPlayer a maximum of one time per invocation, since if"
                            f"you set it again you override the previously set one.")

        raise_if_variable_not_expected_type(value=audioPlayer, expected_type=AudioPlayer, variable_name="audioPlayer")
        self._audioPlayer = audioPlayer
        self.parent_handler_input.alexa.response.directives.append(audioPlayer)

        from inoft_vocal_framework.platforms_handlers.alexa.audioplayer.audioplayer_handlers import AlexaAudioPlayerHandlers
        self.parent_handler_input.alexa.save_audioplayer_handlers_group_class(handlers_group_class_type=AlexaAudioPlayerHandlers)

    def play(self, identifier: str, mp3_file_url: str, title: str, subtitle: str = None, icon_image_url: str = None, background_image_url: str = None,
             offset_in_milliseconds: int = 0, play_behavior: str = AudioPlayer.PLAY_BEHAVIOR_REPLACE_ALL, should_end_session: bool = True):
        # todo: check validity of mp3_file_url

        audio_item = AudioItemObject(identifier=identifier)
        audio_item.mp3_file_url = mp3_file_url
        audio_item.title = title
        audio_item.subtitle = subtitle
        audio_item.icon_image_url = icon_image_url
        audio_item.background_image_url = background_image_url
        audio_item.offset_in_milliseconds = offset_in_milliseconds

        self.audioPlayer = AudioPlayer(played_type=AudioPlayer.TYPE_PLAY, play_behavior=play_behavior,
                                       token_identifier=audio_item.identifier, url=audio_item.mp3_file_url,
                                       offsetInMilliseconds=audio_item.offset_in_milliseconds)

        self.memorize_audio_item(audio_item=audio_item)
        self.id_last_played_item = audio_item.identifier
        self.parent_handler_input.alexa.end_session(should_end=should_end_session)

    def play_item(self, audio_item: AudioItemObject, play_behavior: str = AudioPlayer.PLAY_BEHAVIOR_REPLACE_ALL, should_end_session: bool = True):
        # todo: check validity of mp3_file_url

        self.audioPlayer = AudioPlayer(played_type=AudioPlayer.TYPE_PLAY, play_behavior=play_behavior,
                                       token_identifier=audio_item.identifier, url=audio_item.mp3_file_url,
                                       offsetInMilliseconds=audio_item.offset_in_milliseconds)

        self.memorize_audio_item(audio_item=audio_item)
        self.id_last_played_item = audio_item.identifier
        self.parent_handler_input.alexa.end_session(should_end=should_end_session)

    def stop(self, should_end_session: bool = False):
        self.audioPlayer = AudioPlayer(played_type=AudioPlayer.TYPE_STOP)
        # todo: remember in database the offset in milliseconds
        self.parent_handler_input.alexa.end_session(should_end=should_end_session)

    def clear_queue(self, also_stop_and_clear_current_played_media: bool = False, should_end_session: bool = False):
        # todo: remember in database that we clear the queue (when the queue will be integrated)
        self.audioPlayer = AudioPlayer(played_type=AudioPlayer.TYPE_CLEAR_QUEUE,
                                       clear_behavior=(AudioPlayer.CLEAR_BEHAVIOR_CLEAR_QUEUE
                                                       if also_stop_and_clear_current_played_media is False
                                                       else AudioPlayer.CLEAR_BEHAVIOR_CLEAR_ALL))
        self.parent_handler_input.alexa.end_session(should_end=should_end_session)

    @property
    def token(self) -> str:
        return self.parent_handler_input.alexa.context.audioPlayer.token

    @property
    def player_activity(self) -> str:
        return self.parent_handler_input.alexa.context.audioPlayer.playerActivity

    @property
    def offset_in_milliseconds(self) -> str:
        return self.parent_handler_input.alexa.context.audioPlayer.offsetInMilliseconds

    @property
    def history(self) -> SafeDict:
        if self._history is None:
            self._history = self.parent_handler_input.persistent_remember(data_key="audioPlayerHistory", specific_object_type=SafeDict)
        return self._history

    def get_last_played_item(self) -> AudioItemObject:
        id_last_played_item = self.id_last_played_item
        if id_last_played_item is not None:
            audio_item_dict = self.history.get("items").get(id_last_played_item).to_dict(default=None)
            if audio_item_dict is not None:
                audio_item_object = AudioItemObject(identifier=id_last_played_item, audio_item_dict=audio_item_dict)
                return audio_item_object
        return None

    @property
    def id_last_played_item(self):
        return self.history.get("idLastPlayedItem").to_str(default=None)

    @id_last_played_item.setter
    def id_last_played_item(self, id_last_played_item: str) -> None:
        raise_if_variable_not_expected_type(value=id_last_played_item, expected_type=str, variable_name="id_last_played_item")
        self.history.put("idLastPlayedItem", id_last_played_item)
        self.parent_handler_input.persistent_memorize(data_key="audioPlayerHistory", data_value=self.history)

    @property
    def history_items_dicts(self) -> list:
        return self.history.get("items").to_list()

    def get_history_items_objects(self) -> list:
        output_items_objects_list = list()
        history_items_dict = self.history_items_dicts
        for i, item in enumerate(history_items_dict):
            output_items_objects_list.append(AudioItemObject(identifier=str(i), audio_item_dict=item))
        return output_items_objects_list

    def memorize_audio_item(self, audio_item: AudioItemObject) -> None:
        self.history.get_set("items", {}).put(audio_item.identifier, audio_item.to_dict())
        self.parent_handler_input.persistent_memorize(data_key="audioPlayerHistory", data_value=self.history)





