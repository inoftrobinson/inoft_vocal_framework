from pydub import AudioSegment

from inoft_vocal_framework.audio_editing.sound import Sound
from inoft_vocal_framework.audio_editing.track import Track
from inoft_vocal_framework.audio_editing.relation import Relation
from inoft_vocal_framework.dummy_object import DummyObject
from typing import List, Optional


class AudioClip:
    def __init__(self):
        self.tracks: List[Track] = list()

    def _render(self) -> AudioSegment:
        if len(self.tracks) > 1:
            id_longer_primary_track = None
            duration_longer_primary_track = 0

            for i, track in enumerate(self.tracks):
                track._audio_segment = track._render()
                if track.is_primary:
                    if track._audio_segment.duration_seconds > duration_longer_primary_track:
                        id_longer_primary_track = i
                        duration_longer_primary_track = track._audio_segment.duration_seconds

            if id_longer_primary_track is not None:
                last_overlayed_audio = self.tracks[id_longer_primary_track]._audio_segment
                self.tracks.pop(id_longer_primary_track)
            else:
                last_overlayed_audio = self.tracks[0]._audio_segment
                self.tracks.pop(0)

            for track in self.tracks:
                last_overlayed_audio = last_overlayed_audio.overlay(track._audio_segment, loop=track.loop_until_primary_tracks_finish)
            return last_overlayed_audio
        elif len(self.tracks) > 0:
            return self.tracks[0]._audio_segment
        else:
            return None

    def _export(self, filepath: str, format_type: str = "mp3"):
        audio_segment_result = self._render()
        if audio_segment_result is not None:
            audio_segment_result.export(out_f=filepath, format=format_type)

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise Exception(f"You can only add Track objects to an AudioClip but you tried to add {track}")
        self.tracks.append(track)

    def __add__(self, track: Track):
        self.add_track(track=track)

    def track(self, name: str) -> Track:
        for track in self.tracks:
            if track.name == name:
                return track
        return DummyObject()


if __name__ == "__main__":
    audioclip = AudioClip()

    track_1 = Track(is_primary=True)

    river_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    river_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/track 43.mp3")
    river_background.change_volume(-6.0)
    river_track.append_sound(river_background)

    forest_track = Track(is_primary=False, loop_until_primary_tracks_finish=True)
    forest_background = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD1  - Animal Sounds/track 95.mp3")
    forest_background.change_volume(-6.0)
    forest_track.append_sound(forest_background)

    background_music_track = Track(is_primary=False, loop_until_primary_tracks_finish=False)
    background_music = Sound(local_filepath="F:/Sons utiles/Musics/Vintage (1940s) French Music/Plus Rien N'Existe - Jean Sablon - Wal-Berg.mp3")
    background_music.change_volume(-8.0)
    background_music_track.append_sound(background_music)

    sound_effects_tracks = Track(is_primary=False, loop_until_primary_tracks_finish=False)
    walking_on_dirt_1 = Sound(local_filepath="F:/Sons utiles/Sound Effects/Walks/407659__nagwense__soft-shoes-walking-on-dirt-road.wav")
    sound_effects_tracks.append_sound(walking_on_dirt_1)

    audioclip.add_track(river_track)
    audioclip.add_track(forest_track)
    audioclip.add_track(background_music_track)
    audioclip.add_track(sound_effects_tracks)
    audioclip._export("F:/Sons utiles/test1.mp3")


    """
    t2 = Track(is_primary=True, loop_until_primary_tracks_finish=True)
    s4 = Sound(local_filepath="F:/Sons utiles/2007/Magix SoundPool Collection/NuMetal_2/Synth/arabiclead3.wav")
    s4.change_volume(-40.0)
    t2.append_sound(s4)

    t1 = Track(is_primary=False)
    s3 = Sound(local_filepath="F:/Sons utiles/2009/LucasFilm Sound Effects Library/LucasFilm Sound Effects Library CD2 - Elements/Track 07 - heavy rain.mp3")
    s3.relation = Relation(parent_sound=s4, seconds_child_start_after_parent_end=-3)
    t1.append_sound(s3)

    a = AudioClip()
    a.add_track(t2)
    a.add_track(t1)
    print(a._export(local_filepath="F:/Sons utiles/Sound Effects/dummy_test2.mp3"))
    """

