from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class PlayedSoundInfos:
    player_start_time: int or float
    player_end_time: int or float
    file_start_time: int or float
    file_end_time: int or float
    total_play_time: int or float


class Time:
    def __init__(self, type_key: str, relationship_parent: Any, offset: Optional[int or float] = None):
        self.type_key = type_key
        self.relationship_parent = relationship_parent
        self.offset = offset or 0

    def __add__(self, offset: int or float):
        new_instance = Time(**self.__dict__)
        new_instance.offset += offset
        return new_instance

    def __sub__(self, offset: int or float):
        new_instance = Time(**self.__dict__)
        new_instance.offset -= offset
        return new_instance

    def serialize(self) -> dict:
        # return {'type': 'until-self-end', 'relationship_parent_id': "", 'offset': 0}
        # todo: add support for different time relation in the rust client

        from inoft_vocal_framework.audio_editing.track import Track
        from inoft_vocal_framework.audio_editing.sound import Sound
        self.relationship_parent: Track or Sound
        return {
            'type': self.type_key,
            'relationship_parent_id': self.relationship_parent.id if self.relationship_parent is not None else None,
            'offset': self.offset
        }


class TrackStartTime(Time):
    def __init__(self, track: Any, offset: Optional[int or float] = None):
        super().__init__(type_key='track_start-time', relationship_parent=track, offset=offset)

    def absolute(self) -> int or float:
        return self.offset


class AudioStartTime(Time):
    def __init__(self, sound: Any, offset: Optional[int or float] = None):
        super().__init__(type_key='audio-clip_start-time', relationship_parent=sound, offset=offset)

    def absolute(self) -> int or float:
        return self.relationship_parent.player_start_time.absolute() + self.offset

class AudioEndTime(Time):
    def __init__(self, sound: Any, offset: Optional[int or float] = None):
        super().__init__(type_key='audio-clip_end-time', relationship_parent=sound, offset=offset)

    def absolute(self) -> int or float:
        return (self.relationship_parent.player_start_time.absolute() + self.relationship_parent.duration_seconds) + self.offset


# todo: does the UntilSelfEnd needs to exist ? Compared to an AudioEndTime pointing to itself ?
class UntilSelfEnd(Time):
    def __init__(self, sound: Any, offset: Optional[int or float] = None):
        super().__init__(type_key='until-self-end', relationship_parent=None, offset=offset)


