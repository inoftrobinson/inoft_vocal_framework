import time
import unittest

from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


"""
    river_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    river_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/track 43.mp3")
    river_background.change_volume(-6.0)
    river_track.append_sound(river_background)

    forest_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    forest_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD1  - Animal Sounds/track 95.mp3")
    forest_background.change_volume(-6.0)
    forest_track.append_sound(forest_background)
"""

class TestSingleFile(unittest.TestCase):
    def test_dynamic_content(self):
        start = time.time()
        audio_block_1 = AudioBlock()

        track_voice = audio_block_1.create_track(primary=True, loop=False)
        voice_sound = track_voice.create_speech(
            text="Je suis un test d'audio dynamique ?",
            voice_key='celine',
            player_start_time=track_voice.player_start_time
        )
        rifle_shots = track_voice.create_sound(
            local_filepath="F:/Sons utiles/Sound Effects/Guns/Automatic/238916__qubodup__rifle-shooting.flac",
            player_start_time=voice_sound.player_end_time + 20, player_end_time=voice_sound.player_end_time + 40
        )

        background_music_track = audio_block_1.create_track(primary=True)
        background_music = background_music_track.create_sound(
            local_filepath="F:/Sons utiles/Musics/Vintage (1940s) French Music/CHANSON FRANCAISE 1930-1940 (192  kbps).mp3",
            player_start_time=background_music_track.player_start_time
        )
        background_music.volume = -1.0

        # played_files: dict = audio_block_1.play()
        # played_example_file_infos: PlayedSoundInfos = played_files['example_file']

        audio_block_1._export("F:/Sons utiles/test1.wav", format_type="wav")

    def test_single_file(self):
        audio_block = AudioBlock()
        track = audio_block.create_track(primary=True)
        track.create_sound(local_filepath="F:/Sons utiles/Sound Effects/Guns/Automatic/238916__qubodup__rifle-shooting.flac", player_start_time=track.player_start_time)
        audio_block._export("F:/Sons utiles/test_single_file.wav", format_type="wav")


if __name__ == '__main__':
    unittest.main()
