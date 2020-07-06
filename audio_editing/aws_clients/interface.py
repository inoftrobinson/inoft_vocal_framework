import os

from inoft_vocal_engine.cli.aws_core import AwsCore

a = 9

from inoft_vocal_engine.audio_editing.sound import Sound


class Interface(AwsCore):
    def __init__(self):
        super().__init__()

    def upload_sound(self, sound: Sound):
        bucket_name = "lebucketavecbenoit"
        region_name = "eu-west-3"
        object_key_name = "test_auto_upload.mp3"

        if os.path.exists(sound.local_filepath):
            self.upload_to_s3(filepath=sound.local_filepath, object_key_name=object_key_name, bucket_name=bucket_name, region_name=region_name)

            if os.path.exists(sound.sound_initializer_frame.filename):
                with open(sound.sound_initializer_frame.filename, 'r') as file:
                    lines = file.read().split("\n")

                last_line_initialization_of_sound_object = lines[sound.sound_initializer_frame.lineno - 1]
                last_line_initialization_of_sound_object.replace(" ", "")
                if last_line_initialization_of_sound_object[-1] == ")":
                    new_last_line = last_line_initialization_of_sound_object.replace(
                        ")", f',\nsource_file_s3_bucket_name=\"{bucket_name}",\n'
                             f'source_file_s3_bucket_region="{region_name}",\n'
                             f'source_file_s3_item_path="{object_key_name}")')
                    lines[sound.sound_initializer_frame.lineno - 1] = new_last_line

                with open(sound.sound_initializer_frame.filename, "w") as file:
                    file.write("\n".join(lines))


if __name__ == "__main__":
    s = Sound(local_filepath="F:/Sons utiles/2007/Magix SoundPool Collection/NuMetal_2/Synth/arabiclead3.wav",
source_file_s3_bucket_name="lebucketavecbenoit",
source_file_s3_bucket_region="eu-west-3",
source_file_s3_item_path="test_auto_upload.mp3")
    Interface().upload_sound(s)


"""
for i in range(10):
    with open(__file__, 'r') as f:
        lines = f.read().split('\n')
        val = int(lines[20].split(' = ')[-1])
        new_line = 'a = {}'.format(i)
        new_file = '\n'.join([new_line] + lines[1:])

    with open(__file__, 'w') as f:
        f.write('\n'.join([new_line] + lines[1:]))

    print("hey")
"""