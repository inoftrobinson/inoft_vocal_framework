from typing import Optional, Dict, List
from uuid import uuid4

from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.models import PlayedSoundInfos, TrackStartTime
from inoft_vocal_framework.audio_editing.sound import Sound, AudioStartTime
from inoft_vocal_engine.practical_logger import message_with_vars


class Track:
    def __init__(self, name: str = None, is_primary: bool = True, loop_until_primary_tracks_finish: bool = False):
        self._id = str(uuid4())
        self._audio_segment = None
        self._sounds: Dict[str, Sound] = dict()
        self.name = name
        self.is_primary = is_primary
        self.loop_until_primary_tracks_finish = loop_until_primary_tracks_finish

    def serialize(self) -> dict:
        serialized_clips: Dict[str, dict] = dict()
        for clip_id, clip_item in self._sounds.items():
            serialized_clips[clip_id] = clip_item.serialize()

        return {
            'clips': serialized_clips
        }

    @property
    def id(self) -> str:
        return self._id

    def _render(self) -> (Optional[AudioSegment], PlayedSoundInfos):
        num_sounds = len(self._sounds)
        if num_sounds == 0:
            return None
        elif num_sounds == 1:
            first_sound: Sound = list(self._sounds.values())[0]
            if first_sound.player_start_time.offset == 0 and first_sound.player_end_time.offset == 0:
                # If there is only one audio file in a track, this audio file is obligatory starting at the start of the
                # track. If the audio file, has strictly no start or end offset, the audio block should simply play the
                # audio file itself without any modification. So, instead of processing the audio, we can simply return
                # the audio_segment to generate the audio block output file. Yet, we still need to generate a new output
                # file, because we properly encode the audio type and resolutions when rendering an audio block.
                return first_sound.audio_segment
        else:
            # played_sound_infos = PlayedSoundInfos()
            track_duration = 0
            for key, sound in self._sounds.items():
                sound_end_time = sound.player_end_time.absolute()
                if sound_end_time > track_duration:
                    track_duration = sound_end_time

            output_audio_segment = AudioSegment.silent(track_duration * 1000)
            for key, sound in self._sounds.items():
                sound_start_time = sound.player_start_time.absolute()
                if sound_start_time is not None:
                    if sound.play_duration > sound.file_duration:
                        # The sound needs to be stretched
                        if sound.stretch_method == Sound.STRETCH_LOOP:
                            sound_processed_audio_segment = AudioSegment.silent(sound.play_duration * 1000)
                            sound_processed_audio_segment = sound_processed_audio_segment.overlay(sound.audio_segment, loop=True)
                        else:
                            raise Exception(message_with_vars(
                                "Requested stretch method not supported.",
                                vars_dict={'requestedStretchMethod': sound.stretch_method}
                            ))
                    else:
                        sound_processed_audio_segment = sound.audio_segment
                    output_audio_segment = output_audio_segment.overlay(sound_processed_audio_segment, position=sound_start_time * 1000)

            return output_audio_segment   #, None  # played_sound_infos

    @property
    def audio_segment(self) -> AudioSegment:
        return self._audio_segment

    def _export(self, filepath: str, format_type: str = "mp3"):
        audio_segment_result = self._render()
        if audio_segment_result is not None:
            audio_segment_result.export(out_f=filepath, format=format_type)

    def create_sound(self, engine_file_key: Optional[str] = None, full_file_url: Optional[str] = None,
                     local_filepath: Optional[str] = None,
                     player_start: Optional[AudioStartTime or TrackStartTime] = None,
                     player_end_time: Optional[AudioStartTime or TrackStartTime] = None,
                     file_start_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
                     file_end_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
                     stretch_method: Sound.STRETCH_LOOP = Sound.STRETCH_LOOP) -> Sound:

        file_url: Optional[str] = None
        if engine_file_key is not None:
            account_id = "b1fe5939-032b-462d-92e0-a942cd445096"
            project_id = "22ac1d08-292d-4f2e-a9e3-20d181f1f58f"
            file_url = f"https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/{account_id}/{project_id}/files/{engine_file_key}.wav"
            if full_file_url is not None:
                print("full_file_url not required and is being overridden by the engine_file_key")
        else:
            file_url = full_file_url

        if file_url is not None and local_filepath is not None:
            raise Exception(f"Cannot specify a file_url or engine_file_key with a local_filepath")

        sound = Sound(
            local_filepath=local_filepath, file_url=file_url,
            player_start_time=player_start, player_end_time=player_end_time,
            file_start_time=file_start_time, file_end_time=file_end_time,
            stretch_method=stretch_method
        )
        self._sounds[sound.id] = sound
        return sound

    def append_sound(self, sound: Sound):
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

    @property
    def start_time(self) -> TrackStartTime:
        return TrackStartTime(track=self, offset=0)
