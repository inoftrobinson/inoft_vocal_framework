from inoft_vocal_framework.audio_editing.track import Track
from typing import List, Optional, Dict
from inoft_vocal_framework.audio_editing.types import FORMAT_TYPE_WAV, FORMAT_TYPE_MP3, OUT_FORMATS_UNION, \
    EXPORT_TARGET_MANAGED_ENGINE, EXPORT_TARGET_LOCAL, EXPORT_TARGETS_UNION


class AudioBlock:
    FORMAT_TYPE_WAV = FORMAT_TYPE_WAV
    FORMAT_TYPE_MP3 = FORMAT_TYPE_MP3
    EXPORT_TARGET_MANAGED_ENGINE = EXPORT_TARGET_MANAGED_ENGINE
    EXPORT_TARGET_LOCAL = EXPORT_TARGET_LOCAL

    def __init__(self):
        self.tracks: List[Track] = list()

    def serialize(self) -> dict:
        serialized_tracks: Dict[str, dict] = dict()
        for track in self.tracks:
            serialized_tracks[track.id] = track.serialize()
        return {'tracks': serialized_tracks}

    def manual_render(
            self, engine_account_id: str, engine_project_id: str, engine_api_key: str, override_engine_base_url: Optional[str],
            num_channels: int, sample_rate: int, bitrate: int, out_filepath: Optional[str] = None,
            format_type: OUT_FORMATS_UNION = FORMAT_TYPE_MP3,
            export_target: EXPORT_TARGETS_UNION = EXPORT_TARGET_MANAGED_ENGINE
    ) -> str:
        from inoft_vocal_framework.audio_engine.audio_engine_wrapper import render
        return render(
            engine_account_id=engine_account_id, engine_project_id=engine_project_id,
            engine_api_key=engine_api_key, override_engine_base_url=override_engine_base_url,
            audio_blocks=[self], num_channels=num_channels, sample_rate=sample_rate, bitrate=bitrate,
            out_filepath=out_filepath, out_format_type=format_type, export_target=export_target
        )

    def create_track(self, primary: bool = True, loop: bool = False) -> Track:
        track = Track(is_primary=primary, loop_until_primary_tracks_finish=loop)
        self.tracks.append(track)
        return track

    def add_track(self, track: Track):
        if not isinstance(track, Track):
            raise Exception(f"You can only add Track objects to an AudioBlock but you tried to add {track}")
        self.tracks.append(track)
        return self

    def add_tracks(self, tracks: List[Track]):
        for track_item in tracks:
            self.add_track(track=track_item)
        return self

    def track(self, name: str) -> Optional[Track]:
        for track in self.tracks:
            # todo: move to a dict
            if track.name == name:
                return track
        return None
