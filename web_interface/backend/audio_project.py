from pydantic import BaseModel
from typing import List


class AudioProject(BaseModel):
    class _Collections(BaseModel):
        class _Tracks(BaseModel):
            class _Model(BaseModel):
                class _Attributes(BaseModel):
                    class _File(BaseModel):
                        name: str
                        webkitRelativePath: str
                        lastModified: int
                        size: int
                        type: str

                    class _Buffer(BaseModel):
                        duration: float
                        length: int
                        sampleRate: int
                        numberOfChannels: int

                    file: _File
                    buffer: _Buffer
                    color: str
                    length: float
                    name: str
                    solo: bool
                    pan: int
                    muted: bool
                    gain: float
                attributes: _Attributes
            models: List[_Model]
        tracks: _Tracks
    projectId: str
    collections: _Collections

    def add_track(self, color: str = "e", gain: float = 1.0, pan: int = 0, solo: bool = False, muted: bool = False):
        dummy = {}
        self.collections.tracks.models.append(
            self._Collections._Tracks._Model(
                attributes=self._Collections._Tracks._Model._Attributes(
                    file=self._Collections._Tracks._Model._Attributes._File(
                        name="e", webkitRelativePath="e", lastModified=0, size=0, type="e"
                    ),
                    buffer=self._Collections._Tracks._Model._Attributes._Buffer(
                        duration=0.0, length=1, sampleRate=1, numberOfChannels=2
                    ),
                    color=color, length=100.0, name="Default", solo=solo, pan=pan, muted=muted, gain=gain
                )
            )
        )


"""
{
  'projectId': 'builtin_text-lbs0Re',
  'Collections': {
    'Tracks': {
      'models': [{
        'attributes': {
          'file': {
            'name': 'jean sablon - alexa.mp3',
            'webkitRelativePath': '',
            'lastModified': 1591264478848.0,
            'size': 1007568.0,
            'type': 'audio/mpeg'
          },
          'color': '#00a0b0',
          'length': 1920.0,
          'name': 'Track 1',
          'solo': False,
          'buffer': {
            'duration': 167.71,
            'length': 7396188.0,
            'sampleRate': 44100.0,
            'numberOfChannels': 2.0
          },
          'pan': 0,
          'muted': False,
          'gain': 1.0
        }
      }]
    }
  }
} & text_project_data = {
 
"""