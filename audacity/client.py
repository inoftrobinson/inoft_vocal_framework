from typing import Optional

from inoft_vocal_framework.audacity.pipeclient import PipeClient


class AudacityClient:
    def __init__(self):
        self.client = PipeClient()

    def set_clip(self, clip_id: int, track_number: Optional[int] = None, seconds_start: Optional[float] = None):
        command = f"SetClip: Clip={clip_id}"
        if track_number is not None:
            command += f" At={track_number}"
        if seconds_start is not None:
            command += f" Start={seconds_start}"
        self.client.write(command)

    def select_next_clip(self):
        self.client.write("SelNextClip:")

    def select_previous_clip(self):
        self.client.write("SelPrevClip:")

    def select_track(self, track_number: int = 0):
        self.client.write(f"SelectTracks: Track={track_number}")

    def import_file(self, filepath: str, track_number: int = 0):
        self.client.write(f"Select: Track={track_number}")
        self.client.write(f"Import2: Filename={filepath}")
        self.set_clip(clip_id=0,)

    def delete_all_audio(self):
        self.client.write("SelectAll:")
        self.client.write("Cut:")

    def delete_all_tracks(self):
        self.client.write("SelectTracks: Track=First TrackCount=Last Mode=Add")
        self.client.write("RemoveTracks:")

    def get_info(self):
        print(self.client.write("GetInfo: Type=Tracks"))


if __name__ == "__main__":
    client = AudacityClient()

    client.select_track(track_number=1)
    client.set_clip(clip_id=0, track_number=0, seconds_start=2.0)

    # client.import_file(filepath="C:/Users/LABOURDETTE/Documents/MAGIX/2020-05-20_01_24.wav")  # "F:/test1.mp3")
    # To note, audacity will only accept wav files, and no spaces can be present in the filepath. So the files must
    # be moved to a temporary folder (if they have spaces) and be converted to wav files if they are not in wav.
    print("done")

