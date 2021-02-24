import os
from pathlib import Path
from typing import Optional
from uuid import uuid4

from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.models import TrackStartTime, AudioStartTime, AudioEndTime, UntilSelfEnd
from inoft_vocal_framework.audio_editing.relation import Relation


class SoundProps:
    STRETCH_LOOP = 'loop'

    def __init__(self):
        pass

class Sound(SoundProps):
    def __init__(self, local_filepath: Optional[str] = None, file_url: Optional[str] = None,
                 volume_gain: Optional[float] = 0.0,
                 player_start_time: Optional[AudioStartTime or TrackStartTime] = None,
                 player_end_time: Optional[AudioStartTime or TrackStartTime] = None,
                 file_start_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
                 file_end_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
                 stretch_method: SoundProps.STRETCH_LOOP = SoundProps.STRETCH_LOOP,
                 source_file_s3_bucket_name: Optional[str] = None, source_file_s3_bucket_region: Optional[str] = None,
                 source_file_s3_item_path: Optional[str] = None,
                 render_file_s3_bucket_name: Optional[str] = None, render_file_s3_bucket_region: Optional[str] = None,
                 render_file_s3_item_path: Optional[str] = None):
        super().__init__()

        self._id = str(uuid4())
        self.local_filepath = local_filepath
        if self.local_filepath is not None and not os.path.exists(self.local_filepath):
            raise Exception(f"No file has not been found at {self.local_filepath}")
        self.file_url = file_url
        self._volume = volume_gain

        self._player_start_time = player_start_time
        self._player_end_time = player_end_time or UntilSelfEnd()
        self._file_start_time = max(file_start_time, 0) if file_start_time is not None else 0
        self._file_end_time = file_end_time
        self._stretch_method = stretch_method

        self._in_use = False
        self._append_sound_after_last_one = True

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'localFilepath': self.local_filepath,
            'fileUrl': self.file_url,
            'volume': self.volume,
            'playerStartTime': self._player_start_time.serialize(),
            'playerEndTime': self._player_end_time.serialize(),
            'fileStartTime': self._file_start_time,
            'fileEndTime': self._file_end_time,
        }

    @property
    def id(self) -> str:
        return self._id

    @property
    def audio_segment(self) -> AudioSegment:
        return self._audio_segment

    @property
    def start_time(self) -> AudioStartTime:
        return AudioStartTime(sound=self, offset=0)

    @property
    def end_time(self) -> AudioEndTime:
        return AudioEndTime(sound=self, offset=0)

    @property
    def player_start_time(self) -> AudioStartTime:
        return self._player_start_time

    @property
    def player_end_time(self) -> AudioEndTime:
        return self._player_end_time

    @property
    def play_duration(self) -> int or float:
        return self.player_end_time.absolute() - self.player_start_time.absolute()

    @property
    def file_start_time(self) -> int or float:
        return self._file_start_time

    @property
    def file_end_time(self) -> int or float:
        if self._file_end_time is None:
            return self.audio_segment.duration_seconds
        else:
            return min(self._file_end_time, self.audio_segment.duration_seconds)

    @property
    def file_duration(self):
        return self.file_end_time - self.file_start_time

    @property
    def stretch_method(self):
        return self._stretch_method

    @property
    def append_sound_after_last_one(self) -> bool:
        return self._append_sound_after_last_one

    @append_sound_after_last_one.setter
    def append_sound_after_last_one(self, append_sound_after_last_one: bool) -> None:
        self._append_sound_after_last_one = append_sound_after_last_one

    def copy(self):
        from copy import deepcopy
        copy = deepcopy(self)
        copy._in_use = False
        return copy

    @property
    def volume(self) -> float:
        return self._volume

    @volume.setter
    def volume(self, volume_gain: float):
        self._volume = volume_gain

    @property
    def duration_seconds(self):
        raise Exception("Not implemented")
        # return self._audio_segment.duration_seconds

    def get_dc_offset(self, channel=1):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.get_dc_offset(channel=channel)
        return self

    def remove_dc_offset(self, channel=None, offset=None):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.remove_dc_offset(channel=channel, offset=offset)
        return self

    def overlay(self, seg, seconds_position=0.0, loop=False, times=None, gain_during_overlay=None):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.overlay(seg=seg, position=seconds_position * 1000, loop=loop, times=times, gain_during_overlay=gain_during_overlay)
        return self

    def append(self, seg, crossfade=100):
        self._audio_segment = self._audio_segment.append(seg=seg, crossfade=crossfade)
        return self

    def fade(self, to_gain=0, from_gain=0, start=None, end=None, duration=None):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.fade(to_gain=to_gain, from_gain=from_gain, start=start, end=end, duration=duration)
        return self

    def fade_out(self, duration):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.fade_out(duration=duration)
        return self

    def fade_in(self, duration):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.fade_in(duration=duration)
        return self

    def reverse(self):
        raise Exception("Not implemented")
        # self._audio_segment = self._audio_segment.reverse()
        return self
