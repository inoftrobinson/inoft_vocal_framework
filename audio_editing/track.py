from typing import List

from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.relation import Relation
from inoft_vocal_framework.audio_editing.sound import Sound


def apply_relation_settings(sound: Sound) -> Sound:
    if sound.relation.parent_sound.seconds_start_time is None:
        raise Exception(f"The parent sound with source found at {sound.relation.parent_sound.local_filepath} is not being\n"
                        f"rendered before the child sound of the relation with source found at {sound.local_filepath}.\n"
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
