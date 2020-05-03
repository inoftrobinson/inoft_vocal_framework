import os
from pathlib import Path
from pydub import AudioSegment
from inoft_vocal_framework.dummy_object import DummyObject
from typing import List

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.platforms_handlers.audio_editing.relation import Relation


class SoundProps:
    def __init__(self):
        pass

class Sound(SoundProps):
    def __init__(self, filepath: str, relation: Relation = None, volume_gain: float = 0.0):
        super().__init__()

        self.filepath = filepath
        if isinstance(self.filepath, AudioSegment):
            # If the filepath arg is overridden and loaded with an audio_segment object, we load him right away.
            # I prefer to override the filepath arg, instead of create a load_from_audio_segment function, to
            # avoid any confusions, and to make it clear this is for backend only.
            self._audio_segment = filepath
        else:
            if not os.path.exists(self.filepath):
                raise Exception(f"No file has not been found at {self.filepath}")
            self._audio_segment = AudioSegment.from_file(self.filepath, Path(self.filepath).suffix.replace(".", ""))

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

def apply_relation_settings(sound: Sound) -> Sound:
    if sound.relation.parent_sound.seconds_start_time is None:
        raise Exception(f"The parent sound with source found at {sound.relation.parent_sound.filepath} is not being\n"
                        f"rendered before the child sound of the relation with source found at {sound.filepath}.\n"
                        f"Please try to set your tracks containing your parent sound before in your AudioClip,\n"
                        f"or in your track try to set your parent sound before adding your child sound\n"
                        f"(the order with which you create relations does not matter)")

    if sound.relation.seconds_child_start_after_parent_start is not None:
        sound.seconds_start_time = sound.relation.parent_sound.seconds_start_time + sound.relation.seconds_child_start_after_parent_start
    elif sound.relation.seconds_child_start_after_parent_end is not None:
        sound.seconds_start_time = sound.relation.parent_sound.seconds_end_time + sound.relation.seconds_child_start_after_parent_end
    elif sound.relation.seconds_child_end_after_parent_start is not None:
        sound.seconds_end_time = sound.relation.parent_sound.seconds_start_time + sound.relation.seconds_child_end_after_parent_start
    elif sound.relation.seconds_child_end_after_parent_end is not None:
        sound.seconds_end_time = sound.relation.parent_sound.seconds_end_time + sound.relation.seconds_child_end_after_parent_end
    return sound

class Track:
    def __init__(self, name: str = None, is_primary: bool = True, loop_until_primary_tracks_finish: bool = False):
        self._audio_segment = None
        self._sounds: List[Sound] = list()
        self.name = name
        self.is_primary = is_primary
        self.loop_until_primary_tracks_finish = loop_until_primary_tracks_finish

    def _render(self) -> AudioSegment:
        if not len(self._sounds) > 0:
            return None
        else:
            self._sounds[0].seconds_start_time = 0.0

        if len(self._sounds) == 1 and self._sounds[0].relation is None:
            return self._sounds[0]._audio_segment
        else:
            audio_in_progress = None
            for i, sound in enumerate(self._sounds):
                if sound.relation is None:
                    if sound.append_sound_after_last_one:
                        sound.seconds_start_time = audio_in_progress.duration_seconds
                else:
                    apply_relation_settings(sound=sound)
                    if audio_in_progress is None:
                        if sound.seconds_start_time > 0:
                            audio_in_progress = AudioSegment.silent((sound.duration_seconds + sound.seconds_start_time) * 1000)
                        elif sound.seconds_start_time < 0:
                            audio_in_progress = AudioSegment.silent((sound.duration_seconds - sound.seconds_start_time) * 1000)

                if sound.seconds_start_time is not None:
                    if audio_in_progress is not None:
                        audio_in_progress = audio_in_progress.overlay(sound._audio_segment, position=sound.seconds_start_time * 1000)
                    else:
                        audio_in_progress = sound._audio_segment

            return audio_in_progress

    def _export(self, filepath: str, format_type: str = "mp3"):
        audio_segment_result = self._render()
        if audio_segment_result is not None:
            audio_segment_result.export(out_f=filepath, format=format_type)

    def append_sound(self, sound: Sound, relation: Relation = None):
        if not isinstance(sound, Sound):
            raise Exception(f"You can only add Sound objects to a Track but you tried to add {sound}")

        if sound._in_use:
            raise Exception(f"The same Sound object can be used only once. If you want, you can create a new "
                            f"instance of the same Sound object, by doing   new_sound = my_sound.copy()")
        sound._in_use = True
        sound.append_sound_after_last_one = True

        self._sounds.append(sound)
        return self

    def append_sounds(self, sounds: list):
        for sound in sounds:
            self.append_sound(sound)
        return self

    def __add__(self, sound: Sound):
        self.append_sound(sound=sound)
        return self


class AudioClip:
    def __init__(self):
        self.tracks: List[Track] = list()

    def _render(self) -> AudioSegment:
        if len(self.tracks) > 1:
            id_longer_primary_track = None
            duration_longer_primary_track = 0

            for i, track in enumerate(self.tracks):
                track._audio_segment = track._render()
                if track.is_primary:
                    if track._audio_segment.duration_seconds > duration_longer_primary_track:
                        id_longer_primary_track = i
                        duration_longer_primary_track = track._audio_segment.duration_seconds

            if id_longer_primary_track is not None:
                last_overlayed_audio = self.tracks[id_longer_primary_track]._audio_segment
                self.tracks.pop(id_longer_primary_track)
            else:
                last_overlayed_audio = self.tracks[0]._audio_segment
                self.tracks.pop(0)

            for track in self.tracks:
                last_overlayed_audio = last_overlayed_audio.overlay(track._audio_segment, loop=track.loop_until_primary_tracks_finish)
            return last_overlayed_audio
        elif len(self.tracks) > 0:
            return self.tracks[0]._audio_segment
        else:
            return None

    def _export(self, filepath: str, format_type: str = "mp3"):
        audio_segment_result = self._render()
        if audio_segment_result is not None:
            audio_segment_result.export(out_f=filepath, format=format_type)

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise Exception(f"You can only add Track objects to an AudioClip but you tried to add {track}")
        self.tracks.append(track)

    def __add__(self, track: Track):
        self.add_track(track=track)

    def track(self, name: str) -> Track:
        for track in self.tracks:
            if track.name == name:
                return track
        return DummyObject()


if __name__ == "__main__":
    t2 = Track(is_primary=True, loop_until_primary_tracks_finish=True)
    s4 = Sound(filepath="F:/Sons utiles/2007/Magix SoundPool Collection/NuMetal_2/Synth/arabiclead3.wav")
    s4.change_volume(-40.0)
    t2.append_sound(s4)

    t1 = Track(is_primary=False)
    s3 = Sound(filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/Track 07 - heavy rain.mp3")
    s3.relation = Relation(parent_sound=s4, seconds_child_start_after_parent_end=-3)
    t1.append_sound(s3)

    a = AudioClip()
    a.add_track(t2)
    a.add_track(t1)
    print(a._export(filepath="F:/Sons utiles/Sound Effects/dummy_test2.mp3"))

