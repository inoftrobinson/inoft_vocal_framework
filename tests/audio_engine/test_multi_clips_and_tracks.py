import os
import time
import unittest

import click

import inoft_vocal_framework
from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.tests.audio_engine.shared import ALEXA_BASE_MANUAL_RENDER_KWARGS


class TestInputFormats(unittest.TestCase):
    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self.framework_dirpath = os.path.dirname(os.path.abspath(inoft_vocal_framework.__file__))
        self.audio_samples_dirpath = os.path.join(self.framework_dirpath, "samples/audio")
        self.audio_dist_dirpath = os.path.join(self.framework_dirpath, "dist/audio")
        if not os.path.exists(self.audio_dist_dirpath):
            os.makedirs(self.audio_dist_dirpath)

    def test_first_track_empty(self):
        audio_block = AudioBlock()
        empty_first_track = audio_block.create_track()
        track_music = audio_block.create_track()
        music = track_music.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_wav_16bit.wav"),
            player_start_time=track_music.player_start_time + 2,
            volume=100
        )
        from inoft_vocal_framework.audio_editing.audio_effects import EqualizerEffect
        # music_2.add_effect(EqualizerEffect())
        """from inoft_vocal_framework.audio_editing.audio_effects import TremoloEffect
        music_2.add_effect(TremoloEffect(gain=1, speed=0.3))"""
        """audio_block.create_track().create_sound(
            local_filepath="F:\Inoft/anvers_1944_project\inoft_vocal_framework\plotters-spectrogram-main/example.wav",
            player_start_time=container_track.player_start_time
        )"""

        out_filepath = os.path.join(self.audio_dist_dirpath, f"test_first_track_empty.wav")
        file_url = audio_block.manual_render(**ALEXA_BASE_MANUAL_RENDER_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_WAV)
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_multi_clips(self):
        audio_block_1 = AudioBlock()
        track_1 = audio_block_1.create_track()
        from inoft_vocal_framework import Speech
        music_1 = track_1.create_sound(
            # engine_file_key="how_much_you_want_her_20s",
            local_filepath="C:/Users/LABOURDETTE/Downloads/Isaac Delusion — How Much (You Want Her) 2017 (LYRICS VIDEO).mp3",
            file_start_time=20,
            file_end_time=25,
            player_start_time=track_1.player_start_time + 10,
            player_end_time=track_1.player_start_time + 20
        )

        voice_sound = track_1.create_speech(
            text="Je suis un test d'audio dynamique ?",
            voice_key='celine',
            player_start_time=track_1.player_start_time + 21,
        )

        music_2 = track_1.create_sound(
            local_filepath="C:/Users/LABOURDETTE/Downloads/ANRI - I Can't Stop The Loneliness.mp3",
            player_start_time=voice_sound.end_time + 5,
            player_end_time=voice_sound.end_time + 20
        )

        out_filepath = os.path.join(self.audio_dist_dirpath, f"multi_clip_test.mp3")
        file_url = audio_block_1.manual_render(**ALEXA_BASE_MANUAL_RENDER_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_clip_formats_and_mono_mp3(self):
        audio_block_1 = AudioBlock()
        track_1 = audio_block_1.create_track()

        sound_1 = track_1.create_sound(
            local_filepath="C:/Users/LABOURDETTE/Downloads/Isaac Delusion — How Much (You Want Her) 2017 (LYRICS VIDEO).mp3",
            file_start_time=0,
            file_end_time=10,
            player_start_time=track_1.player_start_time,
            player_end_time=track_1.player_start_time + 5
        )
        sound_2 = track_1.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_wav_16bit.wav"),
            file_start_time=20,
            file_end_time=25,
            player_start_time=sound_1.end_time + 1,
            player_end_time=sound_1.end_time + 6
        )
        sound_3 = track_1.create_sound(
            local_filepath=os.path.join(self.audio_samples_dirpath, "hop_short_mono_mp3.mp3"),
            file_start_time=20,
            file_end_time=25,
            player_start_time=sound_2.end_time + 1,
            player_end_time=sound_2.end_time + 6
        )

        out_filepath = os.path.join(self.audio_dist_dirpath, f"test_clip_formats_and_mono_mp3.mp3")
        file_url = audio_block_1.manual_render(**ALEXA_BASE_MANUAL_RENDER_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))

    def test_clip_reuse(self):
        filepath = os.path.join(self.audio_samples_dirpath, "hop_short_wav_16bit.wav")
        audio_block_1 = AudioBlock()
        track_1 = audio_block_1.create_track()

        sound_1 = track_1.create_sound(
            local_filepath=filepath,
            file_start_time=20,
            file_end_time=30,
            player_start_time=track_1.player_start_time,
            player_end_time=track_1.player_start_time + 5
        )
        sound_2 = track_1.create_sound(
            local_filepath=filepath,
            file_start_time=10,
            file_end_time=18,
            player_start_time=sound_1.end_time + 1,
            player_end_time=sound_1.end_time + 6
        )
        sound_3 = track_1.create_sound(
            local_filepath=filepath,
            file_start_time=30,
            file_end_time=35,
            player_start_time=sound_2.end_time + 1,
            player_end_time=sound_2.end_time + 6
        )

        out_filepath = os.path.join(self.audio_dist_dirpath, f"test_clip_reuse.mp3")
        file_url = audio_block_1.manual_render(**ALEXA_BASE_MANUAL_RENDER_KWARGS, out_filepath=out_filepath, format_type=AudioBlock.FORMAT_TYPE_MP3)
        if click.confirm("Open file ?"):
            os.startfile(out_filepath)
            self.assertTrue(click.confirm(text="Everything's good ?"))



if __name__ == '__main__':
    unittest.main()
