from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class PlayedSoundInfos:
    player_start_time: int or float
    player_end_time: int or float
    file_start_time: int or float
    file_end_time: int or float
    total_play_time: int or float


@dataclass
class Time:
    offset: int or float

    def __add__(self, offset: int or float):
        new_instance = self.__class__(**self.__dict__)
        new_instance.offset += offset
        return new_instance

    @abstractmethod
    def absolute(self) -> int or float:
        raise Exception(f"Not implemented")


@dataclass
class TrackStartTime(Time):
    track: Any

    def absolute(self) -> int or float:
        return self.offset

@dataclass
class AudioStartTime(Time):
    sound: Any

    def absolute(self) -> int or float:
        return self.sound.player_start_time.absolute() + self.offset

@dataclass
class AudioEndTime(Time):
    sound: Any

    def absolute(self) -> int or float:
        return (self.sound.player_start_time.absolute() + self.sound.duration_seconds) + self.offset


