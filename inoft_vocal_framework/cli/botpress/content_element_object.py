from typing import List, Optional

from pydantic import BaseModel

from inoft_vocal_engine.exceptions import raise_if_variable_not_expected_type, raise_if_variable_not_expected_type_and_not_none
from inoft_vocal_engine.inoft_vocal_markup.deserializer import DialogueLine


class ContentElement(BaseModel):
    id: str = None
    created_by: str = None
    created_on: str = None
    modified_on: str = None
    dialogues_lines: Optional[List[DialogueLine]] = None
