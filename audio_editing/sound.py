import os
from pathlib import Path
from typing import Optional
from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.models import TrackStartTime, AudioStartTime, AudioEndTime
from inoft_vocal_framework.audio_editing.relation import Relation


class SoundProps:
    STRETCH_LOOP = 'loop'

    def __init__(self):
        pass

class Sound(SoundProps):
    def __init__(self, local_filepath: str, custom_key: Optional[str] = None, volume_gain: Optional[float] = 0.0,
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

        from inspect import stack
        self.sound_initializer_frame = stack()[1]

        self.key: Optional[str] = None
        self.local_filepath = local_filepath
        if isinstance(self.local_filepath, AudioSegment):
            # If the local_filepath arg is overridden and loaded with an audio_segment object, we load him right away.
            # I prefer to override the local_filepath arg, instead of create a load_from_audio_segment function, to
            # avoid any confusions, and to make it clear this is for backend only.
            self._audio_segment = local_filepath
            if custom_key is not None:
                self.key = custom_key
            else:
                raise Exception(f"When providing an AudioSegment to a sound, a custom_key must also be provided.")
        else:
            if self.local_filepath is None or not os.path.exists(self.local_filepath):
                raise Exception(f"No file has not been found at {self.local_filepath}")
            filepath_path = Path(self.local_filepath)
            self.key = filepath_path.name
            file_format = filepath_path.suffix.replace(".", "")
            print(file_format)
            self._audio_segment = AudioSegment.from_file(file=self.local_filepath, format=file_format)

        self.change_volume(volume_gain=volume_gain)

        self._player_start_time = player_start_time
        self._player_end_time = player_end_time or AudioEndTime(sound=self, offset=0)
        self._file_start_time = max(file_start_time, 0) if file_start_time is not None else 0
        self._file_end_time = file_end_time
        self._stretch_method = stretch_method

        self._in_use = False
        self._append_sound_after_last_one = True

    def serialize(self) -> dict:
        return {
            'localFilepath': self.local_filepath,
            'playerStartTime': self._player_start_time,
            'playerEndTime': self._player_end_time,
            'fileStartTime': self._file_start_time,
            'fileEndTime': self._file_end_time,
        }

    @property
    def audio_segment(self) -> AudioSegment:
        return self._audio_segment

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
        # raise_if_variable_not_expected_type(value=append_sound_after_last_one, expected_type=bool, variable_name="append_sound_after_last_one")
        self._append_sound_after_last_one = append_sound_after_last_one

    def copy(self):
        from copy import deepcopy
        copy = deepcopy(self)
        copy._in_use = False
        return copy

    def change_volume(self, volume_gain: float = 0.0) -> None:
        if volume_gain != 0.0:
            self._audio_segment = self._audio_segment.apply_gain(volume_change=volume_gain)

    def __len__(self):
        return self._audio_segment.__len__()

    def __eq__(self, other):
        return self._audio_segment.__eq__(other=other)

    def __hash__(self):
        return self._audio_segment.__hash__()

    def __ne__(self, other):
        return self._audio_segment.__ne__(other=other)

    def __iter__(self):
        return self._audio_segment.__iter__()

    def __getitem__(self, millisecond):
        return Sound(self._audio_segment.__getitem__(millisecond=millisecond))

    def get_sample_slice(self, start_sample=None, end_sample=None):
        return self._audio_segment.get_sample_slice(start_sample=start_sample, end_sample=end_sample)

    def __add__(self, arg):
        return self._audio_segment.__add__(arg=arg)

    def __radd__(self, rarg):
        return self._audio_segment.__radd__(rarg=rarg)

    def __sub__(self, arg):
        return self._audio_segment.__sub__(arg=arg)

    def __mul__(self, arg):
        return self._audio_segment.__mul__(arg=arg)

    @property
    def duration_seconds(self):
        return self._audio_segment.duration_seconds

    def get_dc_offset(self, channel=1):
        self._audio_segment = self._audio_segment.get_dc_offset(channel=channel)
        return self

    def remove_dc_offset(self, channel=None, offset=None):
        self._audio_segment = self._audio_segment.remove_dc_offset(channel=channel, offset=offset)
        return self

    def overlay(self, seg, seconds_position=0.0, loop=False, times=None, gain_during_overlay=None):
        self._audio_segment = self._audio_segment.overlay(seg=seg, position=seconds_position * 1000, loop=loop, times=times, gain_during_overlay=gain_during_overlay)
        return self

    def append(self, seg, crossfade=100):
        self._audio_segment = self._audio_segment.append(seg=seg, crossfade=crossfade)
        return self

    def fade(self, to_gain=0, from_gain=0, start=None, end=None, duration=None):
        self._audio_segment = self._audio_segment.fade(to_gain=to_gain, from_gain=from_gain, start=start, end=end, duration=duration)
        return self

    def fade_out(self, duration):
        self._audio_segment = self._audio_segment.fade_out(duration=duration)
        return self

    def fade_in(self, duration):
        self._audio_segment = self._audio_segment.fade_in(duration=duration)
        return self

    def reverse(self):
        self._audio_segment = self._audio_segment.reverse()
        return self
