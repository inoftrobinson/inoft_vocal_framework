import unittest


BLACK_SAUCER_URL = "https://inoft-internal-use-only.s3.eu-west-3.amazonaws.com/Black+Saucers.mp3"


class TestResample(unittest.TestCase):
    def test_resample_from_url(self):
        from inoft_vocal_framework.audio_engine.audio_engine_wrapper import resample_save_file_from_url
        success = resample_save_file_from_url(
            file_url=BLACK_SAUCER_URL,
            out_filepath='../../dist/audio/resampled_black_saucer.mp3',
            num_channels=1, sample_rate=24000, bitrate=48, out_format_type='mp3'
        )
        self.assertTrue(success)

    def test_resample_from_local_file(self):
        from inoft_vocal_framework.audio_engine.audio_engine_wrapper import resample_save_file_from_local_file
        success = resample_save_file_from_local_file(
            source_filepath="../../samples/audio/hop_short_wav_32bit.wav",
            out_filepath="../../dist/audio/resampled_hop_show_wav_32bit.mp3",
            num_channels=1, sample_rate=24000, bitrate=48, out_format_type='mp3'
        )
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
