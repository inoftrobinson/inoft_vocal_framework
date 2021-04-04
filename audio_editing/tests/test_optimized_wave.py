import time
import unittest
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


class TestSingleFile(unittest.TestCase):
    def test_optimized_wave(self):
        start = time.time()
        audio_block_1 = AudioBlock()

        primary_track = audio_block_1.create_track(primary=True, loop=False)
        ambiance_sound = primary_track.create_sound(
            local_filepath="F:/Sons utiles/ambiance_out.wav",
            player_start_time=primary_track.start_time + 0, player_end_time=primary_track.start_time + 0
        )
        background_music_sound = primary_track.create_sound(
            local_filepath="F:/Sons utiles/Pour Vous J'Avais Fait Cette Chanson - Jean Sablon.wav",
            player_start_time=primary_track.start_time
        )

        # played_files: dict = audio_block_1.play()
        # played_example_file_infos: PlayedSoundInfos = played_files['example_file']

        audio_block_1._export("F:/Sons utiles/text_optimized_wav_1.mp3", format_type="mp3")

        print(f"execution time = {time.time() - start}")

if __name__ == '__main__':
    unittest.main()
