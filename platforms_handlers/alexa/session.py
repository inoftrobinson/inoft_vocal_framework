from pydantic.main import BaseModel
from typing import Optional


class Session(BaseModel):
    new: bool
    sessionId: str
    application: dict
    user: dict
    attributes: Optional[dict] = None
