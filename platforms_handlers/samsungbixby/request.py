from typing import Optional, Any, List

from pydantic import Field
from pydantic.main import BaseModel

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.formatters import normalize_intent_name


class Request(BaseModel):
    LaunchKeyName = "launch"

    class ContextModel(BaseModel):
        userId: Optional[str] = None
        sessionId: Optional[str] = None
        parameters: Optional[dict] = None

    context: ContextModel = Field(default_factory=ContextModel)
    intent: Optional[str] = None
    parameters: Optional[dict] = None

    def is_launch_request(self):
        return True if self.intent == self.LaunchKeyName else False

    def active_intent_name(self) -> str:
        return normalize_intent_name(intent_name=self.intent)

    def is_in_intent_names(self, intent_names_list: List[str] or str) -> bool:
        intent_name: str = self.active_intent_name()
        if isinstance(intent_names_list, list):
            return intent_name in [normalize_intent_name(intent_name=name) for name in intent_names_list]
        elif isinstance(intent_names_list, str):
            return intent_name == normalize_intent_name(intent_name=intent_names_list)
        else:
            raise Exception(f"intent_names_list type not supported : {type(intent_names_list)}")

    def get_intent_parameter_value(self, parameter_key: str, default=None) -> Any:
        return self.parameters.get(parameter_key, default=default)
