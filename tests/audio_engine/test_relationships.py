import os
import time
import unittest
import webbrowser

import click

import inoft_vocal_framework
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.tests.audio_engine.shared import ALEXA_MANUAL_RENDER_CLOUD_KWARGS


class TestInputFormats(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.framework_dirpath = os.path.dirname(os.path.abspath(inoft_vocal_framework.__file__))
        self.audio_samples_dirpath = os.path.join(self.framework_dirpath, "samples/audio")
        self.audio_dist_dirpath = os.path.join(self.framework_dirpath, "dist/audio")
        if not os.path.exists(self.audio_dist_dirpath):
            os.makedirs(self.audio_dist_dirpath)

    def test_simple(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track2 = audio_block.create_track(primary=True)
        track1.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/Moby+-+Creep+(Radiohead's+cover)+-+trimmed.mp3",
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 20
        )
        track2.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/Joe+Cocker+-+You+Can+Leave+Your+Hat+On+(Official+Video)+HD.mp3",
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 20
        )
        out_filepath = os.path.join(self.audio_dist_dirpath, f"test_simple_relationships.wav")
        response_data: dict = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            webbrowser.open(response_data['fileUrl'])
            self.assertTrue(click.confirm(text="Everything's good ?"))


if __name__ == '__main__':
    unittest.main()
