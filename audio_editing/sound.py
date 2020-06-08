import os
from pathlib import Path
from typing import Optional

from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.relation import Relation
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type


class SoundProps:
    def __init__(self):
        pass

class Sound(SoundProps):
    def __init__(self, local_filepath: str, relation: Optional[Relation] = None, volume_gain: Optional[float] = 0.0,
                 source_file_s3_bucket_name: Optional[str] = None, source_file_s3_bucket_region: Optional[str] = None,
                 source_file_s3_item_path: Optional[str] = None,
                 render_file_s3_bucket_name: Optional[str] = None, render_file_s3_bucket_region: Optional[str] = None,
                 render_file_s3_item_path: Optional[str] = None):
        super().__init__()

        from inspect import stack, getmodule
        self.sound_initializer_frame = stack()[1]

        self.local_filepath = local_filepath
        if isinstance(self.local_filepath, AudioSegment):
            # If the local_filepath arg is overridden and loaded with an audio_segment object, we load him right away.
            # I prefer to override the local_filepath arg, instead of create a load_from_audio_segment function, to
            # avoid any confusions, and to make it clear this is for backend only.
            self._audio_segment = local_filepath
        else:
            if self.local_filepath is None or not os.path.exists(self.local_filepath):
                raise Exception(f"No file has not been found at {self.local_filepath}")
            self._audio_segment = AudioSegment.from_file(self.local_filepath, Path(self.local_filepath).suffix.replace(".", ""))

        self.change_volume(volume_gain=volume_gain)

        self._in_use = False
        self._relation = relation
        self._append_sound_after_last_one = True

        self._seconds_start_time = None
        self._seconds_end_time = None

    @property
    def seconds_start_time(self) -> float:
        if self._seconds_start_time is None and self._seconds_end_time is not None:
            self._seconds_start_time = self._seconds_end_time - self.duration_seconds
        return self._seconds_start_time

    @seconds_start_time.setter
    def seconds_start_time(self, seconds: float) -> None:
        raise_if_variable_not_expected_type(value=seconds, expected_type=float, variable_name="seconds_start_time")
        self._seconds_start_time = seconds

    @property
    def seconds_end_time(self) -> float:
        if self._seconds_end_time is None and self._seconds_start_time is not None:
            self._seconds_end_time = self._seconds_start_time + self.duration_seconds
        return self._seconds_end_time

    @seconds_end_time.setter
    def seconds_end_time(self, seconds: float) -> None:
        raise_if_variable_not_expected_type(value=seconds, expected_type=float, variable_name="seconds_end_time")
        self._seconds_end_time = seconds

    @property
    def relation(self) -> Relation:
        return self._relation

    @relation.setter
    def relation(self, relation: Relation) -> None:
        raise_if_variable_not_expected_type(value=relation, expected_type=Relation, variable_name="relation")
        self._relation = relation

    @property
    def append_sound_after_last_one(self) -> bool:
        return self._append_sound_after_last_one

    @append_sound_after_last_one.setter
    def append_sound_after_last_one(self, append_sound_after_last_one: bool) -> None:
        raise_if_variable_not_expected_type(value=append_sound_after_last_one, expected_type=bool, variable_name="append_sound_after_last_one")
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
