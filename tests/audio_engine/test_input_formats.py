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

    def _base_test(self, filename: str, format_type: str):
        audio_block_1 = AudioBlock()
        background_music_track = audio_block_1.create_track(primary=True)
        background_music_track.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, filename),
            player_start_time=background_music_track.start_time + 2,
            player_end_time=background_music_track.start_time + 30
        )
        out_filepath = os.path.join(self.audio_dist_dirpath, f"temp_test.{format_type}")
        file_url = audio_block_1.render_2(out_filepath=out_filepath, format_type="mp3")
        os.startfile(out_filepath)
        self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_mp3(self):
        self._base_test(filename="hop_short_mp3.mp3", format_type="mp3")

    def test_wav_16bit(self):
        self._base_test(filename="hop_short_wav_16bit.wav", format_type="wav")

    def test_wav_24bit(self):
        self._base_test(filename="hop_short_wav_24bit.wav", format_type="wav")

    def test_wav_32bit(self):
        self._base_test(filename="hop_short_wav_32bit.wav", format_type="wav")

    def test_flac(self):
        self._base_test(filename="hop_short_flac_quality5_16bitdepth.flac", format_type="flac")

    def test_ogg(self):
        self._base_test(filename="hop_short_ogg_quality5.ogg", format_type="ogg")


if __name__ == '__main__':
    unittest.main()
