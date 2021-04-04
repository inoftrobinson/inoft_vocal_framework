from typing import Optional, Dict, List
from uuid import uuid4
from inoft_vocal_framework.audio_editing.models import TrackStartTime
from inoft_vocal_framework.audio_editing.sound import Sound, AudioStartTime


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

    @property
    def player_start_time(self) -> TrackStartTime:
        return TrackStartTime(track=self, offset=0)

    def add_sound(self, sound: Sound):
        if not isinstance(sound, Sound):
            raise Exception(f"You can only add Sound objects to a Track but you tried to add {sound}")

        if sound._in_use:
            raise Exception(f"The same Sound object can be used only once. If you want, you can create a new "
                            f"instance of the same Sound object, by doing   new_sound = my_sound.copy()")
        sound._in_use = True
        sound.append_sound_after_last_one = True
        self._sounds[sound.id] = sound
        return self

    def append_sounds(self, sounds: List[Sound]):
        for sound_item in sounds:
            self.add_sound(sound=sound_item)
        return self

    def create_sound(
            self, engine_file_key: Optional[str] = None, file_url: Optional[str] = None, local_filepath: Optional[str] = None,
            player_start_time: Optional[AudioStartTime or TrackStartTime] = None,
            player_end_time: Optional[AudioStartTime or TrackStartTime] = None,
            file_start_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
            file_end_time: Optional[int or float or AudioStartTime or TrackStartTime] = None,
            stretch_method: Sound.STRETCH_LOOP = Sound.STRETCH_LOOP, speech: bool = False
    ) -> Sound:

        if engine_file_key is not None:
            if file_url is not None:
                print("file_url not required and is being overridden by the engine_file_key")
            account_id = "b1fe5939-032b-462d-92e0-a942cd445096"
            project_id = "22ac1d08-292d-4f2e-a9e3-20d181f1f58f"
            file_url = f"https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/{account_id}/{project_id}/files/{engine_file_key}"

        if file_url is not None and local_filepath is not None:
            raise Exception(f"Cannot specify a file_url or engine_file_key with a local_filepath")

        sound = Sound(
            local_filepath=local_filepath, file_url=file_url,
            player_start_time=player_start_time, player_end_time=player_end_time,
            file_start_time=file_start_time, file_end_time=file_end_time,
            stretch_method=stretch_method
        )
        self.add_sound(sound=sound)
        return sound

    def create_speech(
            self, text: str, voice_key: str,
            player_start_time: Optional[AudioStartTime or TrackStartTime] = None,
            player_end_time: Optional[AudioStartTime or TrackStartTime] = None
    ):
        # todo: implement create_speech
        print(f"Should create speech for {text}")

