import time
from inoft_vocal_framework.audio_editing.track import Track
from typing import List, Optional, Dict


class AudioBlock:
    FORMAT_TYPE_WAV = 'wav'
    FORMAT_TYPE_MP3 = 'mp3'

    def __init__(self):
        self.tracks: List[Track] = list()

    def serialize(self) -> dict:
        serialized_tracks: Dict[str, dict] = dict()
        for track in self.tracks:
            serialized_tracks[track.id] = track.serialize()
        return {'tracks': serialized_tracks}

    def manual_render(
            self, num_channels: int, sample_rate: int, bitrate: int,
            out_filepath: str, format_type: FORMAT_TYPE_MP3 or FORMAT_TYPE_WAV = FORMAT_TYPE_MP3
    ) -> str:
        from inoft_vocal_framework.audio_engine.audio_engine_wrapper import render
        return render(
            audio_blocks=[self],
            num_channels=num_channels, sample_rate=sample_rate, bitrate=bitrate,
            out_filepath=out_filepath, out_format_type=format_type
        )

    def create_track(self, primary: bool = True, loop: bool = False) -> Track:
        track = Track(is_primary=primary, loop_until_primary_tracks_finish=loop)
        self.tracks.append(track)
        return track

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise Exception(f"You can only add Track objects to an AudioBlock but you tried to add {track}")
        self.tracks.append(track)
        return self

    def add_tracks(self, tracks: List[Track]):
        for track_item in tracks:
            self.add_track(track=track_item)
        return self

    def track(self, name: str) -> Optional[Track]:
        for track in self.tracks:
            # todo: move to a dict
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
    ), custom_key="voice", player_start_time=track_voice.start_time)
    rifle_shots = track_voice.create_sound(
        local_filepath="F:/Sons utiles/Sound Effects/Guns/Automatic/238916__qubodup__rifle-shooting.flac",
        player_start_time=voice_sound.player_end_time + 20, player_end_time=voice_sound.player_end_time + 40
    )

    background_music_track = audio_block_1.create_track(primary=True)
    background_music = background_music_track.create_sound(
        local_filepath="F:/Sons utiles/Musics/Vintage (1940s) French Music/CHANSON FRANCAISE 1930-1940 (192  kbps).mp3",
        player_start_time=background_music_track.start_time
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

