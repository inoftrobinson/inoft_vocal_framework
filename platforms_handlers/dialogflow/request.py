from typing import Optional, List
from pydantic import Field
from pydantic.main import BaseModel


class Intent(BaseModel):
    name: str
    displayName: str


class User(BaseModel):
    _VERIFICATION_NAME_GUEST = "GUEST"
    _VERIFICATION_NAME_VERIFIED = "VERIFIED"
    _PERMISSION_UPDATE_TYPE = "UPDATE"

    permissions: Optional[list] = None
    locale: Optional[str] = None
    lastSeen: Optional[str] = None
    userStorage: Optional[str] = None
    userVerificationStatus: Optional[str] = None


class Payload(BaseModel):
    _INPUT_TYPE_OPTION = "OPTION"

    user: User = Field(default_factory=User)

    class Conversation(BaseModel):
        conversationId: str
        type: str
    conversation: Optional[Conversation] = None
    isInSandbox: bool
    requestType: str

    class InputsCustomList(list):
        # todo: make the check that the current device has the capabilities to use an interactive list
        class InputItem(BaseModel):
            intent: str
            rawInputs: list

            class ArgumentItemsCustomList(list):
                class ArgumentItem(BaseModel):
                    name: str
                    textValue: str
                    rawText: str

                def append(self, item: dict) -> None:
                    if isinstance(item, dict):
                        argument_item_object = self.ArgumentItem(**item)
                        super().append(argument_item_object)

                def custom_set_from(self, list_object: list) -> None:
                    for item in list_object:
                        self.append(item=item)

            arguments: Optional[ArgumentItemsCustomList] = Field(default_factory=ArgumentItemsCustomList)

        def append(self, item: dict) -> None:
            if isinstance(item, dict):
                input_item_object = self.InputItem(**item)
                super().append(input_item_object)

        def custom_set_from(self, list_object: list) -> None:
            for item in list_object:
                self.append(item=item)
    inputs: InputsCustomList = Field(default_factory=InputsCustomList)

    class Surface(BaseModel):
        capabilities: list = Field(default_factory=list)
    surface: Surface = Field(default_factory=Surface)

    class AvailableSurfaceItem(BaseModel):
        capabilities: list = Field(default_factory=list)
    availableSurfaces: List[AvailableSurfaceItem] = Field(default_factory=list)

    def get_first_input_of_type(self, type_name: str) -> Optional[dict]:
        for input_item in self.inputs:
            for argument_item in input_item.arguments:
                if argument_item.name == type_name:
                    return argument_item
        return None


class OriginalDetectIntentRequest(BaseModel):
    source: str
    version: str
    payload: Payload


class QueryResult(BaseModel):
    queryText: str
    action: str
    parameters: dict
    allRequiredParamsPresent: bool
    fulfillmentText: Optional[str] = None
    fulfillmentMessages: Optional[List[str]] = None
    outputContexts: List[dict]
    intent: Intent
    intentDetectionConfidence: Optional[int] = None
    diagnosticInfo: Optional[dict] = None
    LanguageModel: str


class Request(BaseModel):
    # General for LaunchRequest, IntentRequest and SessionEndedRequest
    responseId: str
    queryResult: QueryResult
    originalDetectIntentRequest: OriginalDetectIntentRequest
    session: str

    def is_option_select_request(self) -> bool:
        return self.queryResult.queryText == "actions_intent_OPTION"

    def get_updates_user_id_if_present(self) -> Optional[str]:
        for output_context in self.queryResult.outputContexts:
            context_parameters: Optional[dict] = output_context.get('parameters', None)
            if context_parameters is not None:
                context_parameters_permission: Optional[bool] = context_parameters.get('PERMISSION')
                if context_parameters_permission is True:
                    context_parameters_updates_user_id: Optional[str] = context_parameters.get('UPDATES_USER_ID', None)
                    if context_parameters_updates_user_id is not None:
                        return context_parameters_updates_user_id
        return None

    def selected_option_identifier(self) -> str:
        argument_item = self.originalDetectIntentRequest.payload.get_first_input_of_type(self.originalDetectIntentRequest.payload._INPUT_TYPE_OPTION)
        if isinstance(argument_item, self.originalDetectIntentRequest.payload.InputsCustomList.InputItem.ArgumentItemsCustomList.ArgumentItem):
            return argument_item.textValue

    def is_launch_request(self) -> bool:
        return self.queryResult.queryText == "GOOGLE_ASSISTANT_WELCOME"

    def is_in_intent_names(self, intent_names_list: list):
        if self.queryResult.intent.displayName.lower() in [name.lower() for name in intent_names_list]:
            return True
        return False

    def get_intent_parameter_value(self, parameter_key: str, default=None):
        return self.queryResult.parameters.get(dict_key=parameter_key).to_any(default=default)

    def is_not_usable(self):
        return False
        if self.type is not None and self.type not in [self.LaunchRequestKeyName, self.IntentRequestKeyName, self.SessionEndedRequestKeyName]:
            raise Exception(f"The request type '{self.type}' is not None or any of the supported types.")

        return False
        if (self._type == str()
        or self._requestId == str()
        or self._timestamp == str()
        or self._locale == str()):
            return True
        else:
            return False

    def to_dict(self) -> dict:
        return self.dict()

