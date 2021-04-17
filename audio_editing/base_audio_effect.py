from typing import Optional


class BaseAudioEffect:
    def serialize(self) -> dict:
        effect_key: Optional[str] = getattr(self, '_KEY', None)
        if effect_key is None:
            raise Exception(f"No _KEY found for effect {self.__class__.__name__}")
        return {'key': effect_key, 'parameters': self.__dict__}
