import time

from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.sound import Sound
from inoft_vocal_framework.audio_editing.track import Track
from inoft_vocal_framework.audio_editing.relation import Relation
from inoft_vocal_framework.dummy_object import DummyObject
from typing import List, Optional, Union


class AudioBlock:
    FORMAT_TYPE_WAV = 'wav'
    FORMAT_TYPE_MP3 = 'mp3'

    def __init__(self):
        self.tracks: List[Track] = list()

    def serialize(self) -> dict:
        serialized_tracks: List[dict] = list()
        for track in self.tracks:
            serialized_tracks.append(track.serialize())
        return {'tracks': serialized_tracks}

    def render_2(self, out_filepath: str, format_type: FORMAT_TYPE_MP3 or FORMAT_TYPE_WAV = FORMAT_TYPE_MP3) -> str:
        from inoft_vocal_framework.inoft_audio_engine_renderer.audio_engine_renderer_wrapping import render
        return render(audio_blocks=[self], out_filepath=out_filepath, out_format_type=format_type)

    def _render(self) -> Optional[AudioSegment]:
        if len(self.tracks) > 0:
            id_longer_primary_track = None
            duration_longer_primary_track = 0

            for i, track in enumerate(self.tracks):
                track._audio_segment = track._render()
                track.audio_segment.export(out_f=f"F:/Sons utiles/track_{i}.mp3", format="mp3")
                if track.is_primary:
                    if track.audio_segment.duration_seconds > duration_longer_primary_track:
                        id_longer_primary_track = i
                        duration_longer_primary_track = track.audio_segment.duration_seconds

            if id_longer_primary_track is not None:
                last_overlayed_audio = self.tracks[id_longer_primary_track].audio_segment
                self.tracks.pop(id_longer_primary_track)
            else:
                last_overlayed_audio = self.tracks[0].audio_segment
                self.tracks.pop(0)

            for track in self.tracks:
                last_overlayed_audio = last_overlayed_audio.overlay(track.audio_segment, loop=track.loop_until_primary_tracks_finish)
            return last_overlayed_audio
        elif len(self.tracks) > 0:
            return self.tracks[0].audio_segment
        else:
            return None

    def _export(self, filepath: str, format_type: str = "mp3"):
        render_start_time = time.time()
        audio_segment_result = self._render()
        if audio_segment_result is not None:
            export_start_time = time.time()
            audio_segment_result.export(out_f=filepath, format=format_type, bitrate="48k")
            print(f"export time : {time.time() - export_start_time}")
            print(f"render & export time : {time.time() - render_start_time}")

    def play(self):
        return
        if len(self.tracks) > 0:
            if id_longer_primary_track is not None:
                last_overlayed_audio = self.tracks[id_longer_primary_track]._audio_segment
                self.tracks.pop(id_longer_primary_track)
            else:
                last_overlayed_audio = self.tracks[0]._audio_segment
                self.tracks.pop(0)

            for track in self.tracks:
                last_overlayed_audio = last_overlayed_audio.overlay(track._audio_segment,
                                                                    loop=track.loop_until_primary_tracks_finish)
            return last_overlayed_audio
        elif len(self.tracks) > 0:
            return self.tracks[0]._audio_segment
        else:
            return None

    def create_track(self, primary: bool = True, loop: bool = False) -> Track:
        track = Track(is_primary=primary, loop_until_primary_tracks_finish=loop)
        self.tracks.append(track)
        return track

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise Exception(f"You can only add Track objects to an AudioBlock but you tried to add {track}")
        self.tracks.append(track)

    def __add__(self, track: Track):
        self.add_track(track=track)

    def track(self, name: str) -> Optional[Track]:
        for track in self.tracks:
            if track.name == name:
                return track
        return None


if __name__ == "__main__":
    start = time.time()
    audio_block_1 = AudioBlock()

    """river_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    river_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/track 43.mp3")
    river_background.change_volume(-6.0)
    river_track.append_sound(river_background)

    forest_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    forest_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD1  - Animal Sounds/track 95.mp3")
    forest_background.change_volume(-6.0)
    forest_track.append_sound(forest_background)"""

    from inoft_vocal_engine.speech_synthesis.polly.client import PollyClient
    from inoft_vocal_engine.speech_synthesis.polly import VOICES

    track_voice = audio_block_1.create_track(primary=True, loop=False)
    voice_sound = track_voice.create_sound(local_filepath=PollyClient().synthesize(
        text="Je suis un test d'audio dynamique ?",
        voice_id=VOICES.French_France_Female_CELINE.id,
        filepath_to_save_to="F:/Sons utiles/test_synthesised_dialogue.mp3"
    ), custom_key="voice", player_start=track_voice.start_time)
    rifle_shots = track_voice.create_sound(
        local_filepath="F:/Sons utiles/Sound Effects/Guns/Automatic/238916__qubodup__rifle-shooting.flac",
        player_start=voice_sound.player_end_time + 20, player_end_time=voice_sound.player_end_time + 40
    )

    background_music_track = audio_block_1.create_track(primary=True)
    background_music = background_music_track.create_sound(
        local_filepath="F:/Sons utiles/Musics/Vintage (1940s) French Music/CHANSON FRANCAISE 1930-1940 (192  kbps).mp3",
        player_start=background_music_track.start_time
    )
    background_music.volume = -1.0

    # played_files: dict = audio_block_1.play()
    # played_example_file_infos: PlayedSoundInfos = played_files['example_file']

    """sound_effects_tracks = Track(is_primary=False, loop_until_primary_tracks_finish=False)
    walking_on_dirt_1 = Sound(local_filepath="F:/Sons utiles/Sound Effects/Walks/407659__nagwense__soft-shoes-walking-on-dirt-road.wav")
    sound_effects_tracks.append_sound(walking_on_dirt_1)"""

    audio_block_1.render_2("F:/Sons utiles/test1.wav", format_type="wav")
    print(time.time() - start)


    """
    t2 = Track(is_primary=True, loop_until_primary_tracks_finish=True)
    s4 = Sound(local_filepath="F:/Sons utiles/2007/Magix SoundPool Collection/NuMetal_2/Synth/arabiclead3.wav")
    s4.change_volume(-40.0)
    t2.append_sound(s4)

    t1 = Track(is_primary=False)
    s3 = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/Track 07 - heavy rain.mp3")
    s3.relation = Relation(parent_sound=s4, seconds_child_start_after_parent_end=-3)
    t1.append_sound(s3)

    a = AudioClip()
    a.add_track(t2)
    a.add_track(t1)
    print(a._export(local_filepath="F:/Sons utiles/Sound Effects/dummy_test2.mp3"))
    """

