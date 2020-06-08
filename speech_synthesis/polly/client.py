"""Getting Started Example for Python 2.7+/3.3+"""
from typing import Optional

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys


class PollyClient:
    def __init__(self):
        session = Session()
        self.client = session.client("polly")

    def synthesize(self, text: str, voice_id: str, filepath_to_save_to: str,
                   output_format: Optional[str] = "mp3", should_play_audio:  Optional[bool] = False):
        try:
            response = self.client.synthesize_speech(Text=text, VoiceId=voice_id, OutputFormat=output_format)
        except (BotoCoreError, ClientError) as error:
            # The service returned an error, exit gracefully
            print(f"Error while synthesising using the voice {voice_id} the following text : {text} - {error}")
            return None

        # Access the audio stream from the response
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                try:
                    # Open a file for writing the output as a binary stream
                    with open(filepath_to_save_to, "wb+") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(f"Error while saving the synthesized speech with the voice {voice_id} of the following text : {text} - {error}")
                    return None

        else:
            # The response didn't contain audio data, exit gracefully
            print(f"AWS Polly did not send AudioDate while synthesizing using the voice {voice_id} the following text : {text}")
            return None

        if should_play_audio is True:
            # Play the audio using the platform's default player
            if sys.platform == "win32":
                os.startfile(filepath_to_save_to)
            else:
                # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
                import subprocess
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, filepath_to_save_to])

        return filepath_to_save_to


if __name__ == "__main__":
    from inoft_vocal_framework.speech_synthesis.polly import VOICES

    PollyClient().synthesize(text="Bien le bonjour l'ami. T'aime le chocolat ?", voice_id=VOICES.Icelandic_Iceland_Male_KARL.id,
                             filepath_to_save_to="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/test.mp3",
                             should_play_audio=True)
