import os
from typing import Optional

from inoft_vocal_framework.audacity.pipeclient import PipeClient


class AudacityClient:
    EXPORT_TYPE_MP3 = "mp3"
    EXPORT_TYPE_WAV = "wav"
    EXPORT_MODE_ALL = "All"
    EXPORT_MODE_SELECTION = "Selection"

    def __init__(self):
        self.client = PipeClient()

    def set_clip(self, clip_id: int, track_number: Optional[int] = None, seconds_start: Optional[float] = None):
        command = f"SetClip: Clip={clip_id}"
        if track_number is not None:
            command += f" At={track_number}"
        if seconds_start is not None:
            command += f" Start={seconds_start}"
        self.client.write(command)

    def select_all(self):
        self.client.write("SelectAll:")

    def select_next_clip(self):
        self.client.write("SelNextClip:")

    def select_previous_clip(self):
        self.client.write("SelPrevClip:")

    def select_track(self, track_number: int = 0):
        self.client.write(f"SelectTracks: Track={track_number} Mode=Add")

    def import_file(self, filepath: str, track_number: int = 0):
        self.client.write(f"Select: Track={track_number}")
        self.client.write(f"Import2: Filename={filepath}")
        # self.set_clip(clip_id=0)

    def delete_all_audio(self):
        self.client.write("SelectAll:")
        self.client.write("Cut:")

    def delete_all_tracks(self):
        self.client.write("SelectTracks: Track=First TrackCount=Last Mode=Add")
        # We add all the tracks from the First to the Last to a selection
        self.client.write("RemoveTracks:")
        # Then we remove the tracks in our selection

    def mix_and_render_all_elements(self):
        self.select_all()
        self.mix_and_render_tracks()

    def mix_and_render_tracks(self):
        self.client.write("MixAndRender:")

    def new_project(self):
        self.client.write("New:")

    def save_project(self, project_output_filepath: str, add_to_history: Optional[bool] = True, compress: Optional[bool] = False):
        if os.path.isfile(project_output_filepath):
            # If audacity try to save a project over an existing file, it might crash
            os.remove(project_output_filepath)
        self.client.write(f"SaveProject2: Filename={project_output_filepath} AddToHistory={add_to_history} Compress={compress}")

    def export(self, filepath: str, num_channels: int = 1, export_mode: str = EXPORT_MODE_ALL):
        self.client.write(f"Export2: Filename={filepath} NumChannels={num_channels}")

    def get_info(self):
        print(self.client.write("GetInfo: Type=Tracks"))


if __name__ == "__main__":
    client = AudacityClient()

    client.mix_and_render_all_elements()
    # client.select_track(track_number=3)
    # client.set_clip(clip_id=0, track_number=0, seconds_start=2.0)

    # client.import_file(filepath="C:/Users/LABOURDETTE/Documents/MAGIX/2020-05-20_01_24.wav")  # "F:/test1.mp3")
    # client.save_project(project_output_filepath="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/speech_synthesis/polly/project.aup")
    # To note, audacity will only accept wav files, and no spaces can be present in the filepath. So the files must
    # be moved to a temporary folder (if they have spaces) and be converted to wav files if they are not in wav.
    print("done")

