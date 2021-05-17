import os
import unittest
import webbrowser

import click

import inoft_vocal_framework
from inoft_vocal_framework import AudioBlock
from inoft_vocal_framework.audio_editing.sound import SpeechSound
from inoft_vocal_framework.audio_editing.track import Track
from inoft_vocal_framework.tests.audio_engine.shared import ALEXA_BASE_MANUAL_RENDER_KWARGS, \
    ALEXA_MANUAL_RENDER_CLOUD_KWARGS


class TestInputFormats(unittest.TestCase):
    def __init__(self, method_name: str):
        super().__init__(methodName=method_name)
        self.framework_dirpath = os.path.dirname(os.path.abspath(inoft_vocal_framework.__file__))
        self.audio_samples_dirpath = os.path.join(self.framework_dirpath, "samples/audio")
        self.audio_dist_dirpath = os.path.join(self.framework_dirpath, "dist/audio")
        if not os.path.exists(self.audio_dist_dirpath):
            os.makedirs(self.audio_dist_dirpath)

    def test_first_track_empty(self):
        audio_block = AudioBlock()
        track: Track = audio_block.create_track()
        speech_sound: SpeechSound = track.create_speech(
            text="Bien le bonjour cher ami. Aimes-tu les cookies ? e", voice_key='Lea',
            player_start_time=track.player_start_time + 2
        )

        out_filepath = os.path.join(self.audio_dist_dirpath, f"test_synthesised_speech.wav")
        file_url = audio_block.manual_render(**ALEXA_BASE_MANUAL_RENDER_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_WAV)
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_hash(self):
        audio_block = AudioBlock()
        track: Track = audio_block.create_track()
        speech_sound: SpeechSound = track.create_speech(
            text="This is my first text.", voice_key='Lea',
            player_start_time=track.player_start_time + 2
        )
        first_file_url: str = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, format_type=AudioBlock.FORMAT_TYPE_MP3)

        audio_block = AudioBlock()
        track: Track = audio_block.create_track()
        speech_sound: SpeechSound = track.create_speech(
            text="This is my second text that should generated a different hash.", voice_key='Lea',
            player_start_time=track.player_start_time + 2
        )
        second_file_url: str = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, format_type=AudioBlock.FORMAT_TYPE_MP3)

        self.assertNotEqual(first_file_url, second_file_url)

        if click.confirm("Open first file ?"):
            webbrowser.open(first_file_url)
            self.assertTrue(click.confirm(text="Everything's good ?"))

        if click.confirm("Open second file ?"):
            webbrowser.open(second_file_url)
            self.assertTrue(click.confirm(text="Everything's good ?"))


if __name__ == '__main__':
    unittest.main()
