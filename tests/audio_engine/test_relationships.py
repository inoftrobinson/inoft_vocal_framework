import os
import time
import unittest
import webbrowser
from typing import Optional

import click

import inoft_vocal_framework
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.tests.audio_engine.shared import ALEXA_MANUAL_RENDER_CLOUD_KWARGS, \
    ALEXA_BASE_MANUAL_RENDER_KWARGS


class TestRelationships(unittest.TestCase):
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
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_wav_16bit.wav"),
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 20
        )
        file_url: Optional[str] = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            webbrowser.open(file_url)
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_ambiguous(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track2 = audio_block.create_track(primary=True)
        sound_1 = track1.create_sound(
            file_url="https://inoft-vocal-engine-web-test.s3.eu-west-3.amazonaws.com/Moby+-+Creep+(Radiohead's+cover)+-+trimmed.mp3",
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 21
        )
        sound_2 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_mp3.mp3"),
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 20
        )
        sound_3 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "synthchopinfantaisieimpromptu120bpm1.mp3"),
            player_start_time=sound_1.player_start_time + 5,
            player_end_time=sound_2.player_end_time - 2
        )
        out_filepath = os.path.join(self.audio_dist_dirpath, "test_relationships_ambiguous")
        response_data: dict = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            webbrowser.open(response_data['fileUrl'])
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_unusual_but_working_relations(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track2 = audio_block.create_track(primary=True)
        sound_1 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_mp3.mp3"),
            player_start_time=track1.player_start_time,
            player_end_time=track2.player_start_time + 20
        )

        # sound_2 is dependant on sound_1.player_start_time

        from inoft_vocal_framework.audio_editing.audio_effects import TremoloEffect
        sound_2 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "synthchopinfantaisieimpromptu120bpm1.mp3"),
            player_start_time=sound_1.player_end_time + 5,
            player_end_time=track2.player_start_time + 25
        )

        # We force sound_1 to be dependant to sound_2
        sound_1._player_start_time = sound_2.player_start_time + 3

        out_filepath = os.path.join(self.audio_dist_dirpath, "test_broken_relations")
        response_data: dict = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            webbrowser.open(response_data['fileUrl'])
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_broken_relation(self):
        audio_block = AudioBlock()
        track1 = audio_block.create_track(primary=True)
        track2 = audio_block.create_track(primary=True)
        sound_1 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_mp3.mp3"),
            player_start_time=track1.player_start_time,
        )

        # sound_2 is dependant on sound_1.player_start_time
        sound_2 = track2.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "synthchopinfantaisieimpromptu120bpm1.mp3"),
            player_start_time=sound_1.player_end_time + 5,
            player_end_time=track2.player_start_time + 25
        )

        # We force sound_1 to be dependant to sound_2
        sound_1._player_start_time = sound_2.player_start_time + 3

        out_filepath = os.path.join(self.audio_dist_dirpath, "test_broken_relations")
        response_data: dict = audio_block.manual_render(**ALEXA_MANUAL_RENDER_CLOUD_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            webbrowser.open(response_data['fileUrl'])
            self.assertTrue(click.confirm(text="Everything's good ?"))


if __name__ == '__main__':
    unittest.main()
