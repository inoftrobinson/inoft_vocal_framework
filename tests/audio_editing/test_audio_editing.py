import time
import unittest

from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


class MyTestCase(unittest.TestCase):
    def test_something(self):
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

        # track_voice = audio_block_1.create_track(primary=True, loop=False)
        """voice_sound = track_voice.create_sound(local_filepath=PollyClient().synthesize(
            text="Je suis un test d'audio dynamique ?",
            voice_id=VOICES.French_France_Female_CELINE.id,
            filepath_to_save_to="F:/Sons utiles/test_synthesised_dialogue.mp3"
        ), custom_key="voice", player_start=track_voice.start_time)"""
        """rifle_shots = track_voice.create_sound(
            local_filepath="F:/Sons utiles/Sound Effects/Guns/Automatic/238916__qubodup__rifle-shooting.flac",
            player_start=voice_sound.player_end_time + 20, player_end_time=voice_sound.player_end_time + 40
        )"""

        background_music_track = audio_block_1.create_track(primary=True)
        background_music = background_music_track.create_sound(
            local_filepath="F:/Sons utiles/Musics/Vintage (1940s) French Music/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav",
            player_start=background_music_track.start_time
        )
        background_music.change_volume(-1.0)
        background_music_track.create_sound(
            local_filepath="F:/Sons utiles/ambiance_out.wav",
            player_start=background_music_track.start_time
        )

        audio_block_1.render_2()


if __name__ == '__main__':
    unittest.main()
