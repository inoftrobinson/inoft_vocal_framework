from abc import abstractmethod
from typing import Optional


class BaseMiddleware:
    _MIDDLEWARE_KEY: Optional[str] = None

    def __init__(self, skill):
        from inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftSkill
        self.skill: InoftSkill = skill

    @property
    def key(self) -> str:
        if self._MIDDLEWARE_KEY is None:
            raise Exception("Middleware key not defined")
        return self._MIDDLEWARE_KEY

    @abstractmethod
    def on_interaction_end(self):
        pass
