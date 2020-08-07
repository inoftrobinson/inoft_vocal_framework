from typing import List, Optional

from pydantic import BaseModel

from inoft_vocal_framework.inoft_vocal_markup.deserializer import DialogueLine


class ContentElement(BaseModel):
    id: str = None
    created_by: str = None
    created_on: str = None
    modified_on: str = None
    dialogues_lines: Optional[List[DialogueLine]] = None
