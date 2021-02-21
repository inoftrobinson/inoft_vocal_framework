import os
import time
import unittest

import click

import inoft_vocal_framework
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock


class TestInputFormats(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.framework_dirpath = os.path.dirname(os.path.abspath(inoft_vocal_framework.__file__))
        self.audio_samples_dirpath = os.path.join(self.framework_dirpath, "samples/audio")
        self.audio_dist_dirpath = os.path.join(self.framework_dirpath, "dist/audio")
        if not os.path.exists(self.audio_dist_dirpath):
            os.makedirs(self.audio_dist_dirpath)

    def test_multi_clips(self):
        audio_block_1 = AudioBlock()
        track_1 = audio_block_1.create_track()
        from inoft_vocal_framework import Speech
        music_1 = track_1.create_sound(
            # engine_file_key="how_much_you_want_her_20s",
            local_filepath="C:/Users/LABOURDETTE/Downloads/Isaac Delusion — How Much (You Want Her) 2017 (LYRICS VIDEO).mp3",
            file_start_time=20,
            file_end_time=25,
            player_start=track_1.start_time + 10,
            player_end_time=track_1.start_time + 20
        )

        from inoft_vocal_engine.speech_synthesis.polly import VOICES
        from inoft_vocal_engine.speech_synthesis.polly.client import SpeechSynthesisClient
        response = SpeechSynthesisClient().synthesize(
            text="Je suis un test d'audio dynamique ?",
            voice_id=VOICES.French_France_Female_CELINE.id
        )
        voice_sound = track_1.create_sound(
            full_file_url=f"https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/{response[1]}",
            player_start=track_1.start_time + 21,
        )

        music_2 = track_1.create_sound(
            local_filepath="C:/Users/LABOURDETTE/Downloads/ANRI - I Can't Stop The Loneliness.mp3",
            player_start=voice_sound.end_time + 5,
            player_end_time=voice_sound.end_time + 20
        )

        out_filepath = os.path.join(self.audio_dist_dirpath, f"multi_clip_test.mp3")
        file_url = audio_block_1.render_2(out_filepath=out_filepath, format_type="mp3")
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))


if __name__ == '__main__':
    unittest.main()
