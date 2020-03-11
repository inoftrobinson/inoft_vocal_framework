from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict


class Intent:
    json_key = "intent"

    def __init__(self):
        self._name = str()
        self._displayName = str()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        if not isinstance(name, str):
            raise Exception(f"name was type {type(name)} which is not valid value for his parameter.")
        self._name = name

    @property
    def displayName(self) -> str:
        return self._displayName

    @displayName.setter
    def displayName(self, displayName: str) -> None:
        if not isinstance(displayName, str):
            raise Exception(f"displayName was type {type(displayName)} which is not valid value for his parameter.")
        self._displayName = displayName

class User:
    json_key = "user"

    VERIFICATION_NAME_GUEST = "GUEST"
    VERIFICATION_NAME_VERIFIED = "VERIFIED"

    def __init__(self):
        self._locale = str()
        self._lastSeen = str()
        self._userStorage = str()
        self._userVerificationStatus = str()

    @property
    def locale(self) -> str:
        return self._locale

    @locale.setter
    def locale(self, locale: str) -> None:
        if not isinstance(locale, str):
            raise Exception(f"locale was type {type(locale)} which is not valid value for his parameter.")
        self._locale = locale

    @property
    def lastSeen(self) -> str:
        return self._lastSeen

    @lastSeen.setter
    def lastSeen(self, lastSeen: str) -> None:
        if not isinstance(lastSeen, str):
            raise Exception(f"lastSeen was type {type(lastSeen)} which is not valid value for his parameter.")
        self._lastSeen = lastSeen

    @property
    def userStorage(self) -> str:
        return self._userStorage

    @userStorage.setter
    def userStorage(self, userStorage: str) -> None:
        if not isinstance(userStorage, str):
            raise Exception(f"userStorage was type {type(userStorage)} which is not valid value for his parameter.")
        self._userStorage = userStorage

    @property
    def userVerificationStatus(self) -> str:
        return self._userVerificationStatus

    @userVerificationStatus.setter
    def userVerificationStatus(self, userVerificationStatus: str) -> None:
        if not isinstance(userVerificationStatus, str):
            raise Exception(f"userVerificationStatus was type {type(userVerificationStatus)} which is not valid value for his parameter.")
        self._userVerificationStatus = userVerificationStatus


class Payload:
    json_key = "payload"

    def __init__(self):
        self._user = User()
        self._conversation = None
        self._inputs = None

    @property
    def user(self) -> User:
        return self._user

class OriginalDetectIntentRequest:
    json_key = "originalDetectIntentRequest"

    def __init__(self):
        self._source = str()
        self._version = str()
        self._payload = Payload()

    @property
    def payload(self) -> Payload:
        return self._payload

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, source: str) -> None:
        if not isinstance(source, str):
            raise Exception(f"source was type {type(source)} which is not valid value for his parameter.")
        self._source = source

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        if not isinstance(version, str):
            raise Exception(f"version was type {type(version)} which is not valid value for his parameter.")
        self._version = version

class QueryResult:
    json_key = "queryResult"

    def __init__(self):
        self._queryText = str()
        self._action = str()
        self._parameters = SafeDict()
        self._allRequiredParamsPresent = bool()
        self._fulfillmentText = str()
        self._fulfillmentMessages = list()
        self._outputContexts = list()
        self._intent = Intent()
        self._intentDetectionConfidence = int()
        self._diagnosticInfo = dict()
        self._languageCode = str()

    @property
    def queryText(self) -> str:
        return self._queryText

    @queryText.setter
    def queryText(self, queryText: str) -> None:
        if isinstance(queryText, str):
            self._queryText = queryText
        else:
            raise Exception(f"queryText was type {type(queryText)} which is not valid value for his parameter.")

    @property
    def action(self) -> str:
        return self._action

    @action.setter
    def action(self, action: str) -> None:
        if isinstance(action, str):
            self._action = action
        else:
            raise Exception(f"action was type {type(action)} which is not valid value for his parameter.")

    @property
    def parameters(self) -> SafeDict:
        if isinstance(self._parameters, dict):
            self._parameters = SafeDict(self._parameters)
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: dict) -> None:
        if not isinstance(parameters, dict):
            raise Exception(f"parameters was type {type(parameters)} which is not valid value for his parameter.")
        self._parameters = SafeDict(parameters)

    @property
    def allRequiredParamsPresent(self) -> bool:
        return self._allRequiredParamsPresent

    @allRequiredParamsPresent.setter
    def allRequiredParamsPresent(self, allRequiredParamsPresent: bool) -> None:
        if isinstance(allRequiredParamsPresent, bool):
            self._allRequiredParamsPresent = allRequiredParamsPresent
        else:
            raise Exception(f"allRequiredParamsPresent was type {type(allRequiredParamsPresent)} which is not valid value for his parameter.")

    @property
    def fulfillmentText(self) -> str:
        return self._fulfillmentText

    @fulfillmentText.setter
    def fulfillmentText(self, fulfillmentText: str) -> None:
        if isinstance(fulfillmentText, str):
            self._fulfillmentText = fulfillmentText
        else:
            raise Exception(f"fulfillmentText was type {type(fulfillmentText)} which is not valid value for his parameter.")

    @property
    def fulfillmentMessages(self) -> list:
        return self._fulfillmentMessages

    @fulfillmentMessages.setter
    def fulfillmentMessages(self, fulfillmentMessages: list) -> None:
        if isinstance(fulfillmentMessages, list):
            self._fulfillmentMessages = fulfillmentMessages
        else:
            raise Exception(f"fulfillmentMessages was type {type(fulfillmentMessages)} which is not valid value for his parameter.")

    @property
    def outputContexts(self) -> list:
        return self._outputContexts

    @outputContexts.setter
    def outputContexts(self, outputContexts: list) -> None:
        if isinstance(outputContexts, list):
            self._outputContexts = outputContexts
        else:
            raise Exception(f"outputContexts was type {type(outputContexts)} which is not valid value for his parameter.")

    @property
    def intent(self) -> Intent:
        return self._intent

    @intent.setter
    def intent(self, intent: Intent) -> None:
        if isinstance(intent, Intent):
            self._intent = intent
        else:
            raise Exception(f"intent was type {type(intent)} which is not valid value for his parameter.")

    @property
    def intentDetectionConfidence(self) -> int:
        return self._intentDetectionConfidence

    @intentDetectionConfidence.setter
    def intentDetectionConfidence(self, intentDetectionConfidence: int) -> None:
        if isinstance(intentDetectionConfidence, int):
            self._intentDetectionConfidence = intentDetectionConfidence
        else:
            raise Exception(f"intentDetectionConfidence was type {type(intentDetectionConfidence)} which is not valid value for his parameter.")

    @property
    def diagnosticInfo(self) -> dict:
        return self._diagnosticInfo

    @diagnosticInfo.setter
    def diagnosticInfo(self, diagnosticInfo: dict) -> None:
        if isinstance(diagnosticInfo, dict):
            self._diagnosticInfo = diagnosticInfo
        else:
            raise Exception(f"diagnosticInfo was type {type(diagnosticInfo)} which is not valid value for his parameter.")

    @property
    def languageCode(self) -> str:
        return self._languageCode

    @languageCode.setter
    def languageCode(self, languageCode: str) -> None:
        if isinstance(languageCode, str):
            self._languageCode = languageCode
        else:
            raise Exception(f"languageCode was type {type(languageCode)} which is not valid value for his parameter.")

class Request:
    json_key = "request"

    def __init__(self):
        # General for LaunchRequest, IntentRequest and SessionEndedRequest
        self._responseId = str()
        self._queryResult = QueryResult()
        self._originalDetectIntentRequest = OriginalDetectIntentRequest()
        self._session = str()

    def process_and_set_json_request_to_object(self, stringed_request_json_dict: str):
        NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self,
                                                                  request_json_dict_stringed_dict_or_list=stringed_request_json_dict)

    def is_launch_request(self) -> bool:
        if self.queryResult.intent.displayName == "LaunchIntentRequest":
            return True
        else:
            return False

    def is_in_intent_names(self, intent_names_list: list):
        if self.queryResult.intent.displayName in intent_names_list:
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
        dict_object = NestedObjectToDict.get_dict_from_nested_object(object_to_process=self,
                                                                     key_names_identifier_objects_to_go_into=["json_key"])
        return dict_object

    @property
    def queryResult(self) -> QueryResult:
        return self._queryResult

    @property
    def originalDetectIntentRequest(self) -> OriginalDetectIntentRequest:
        return self._originalDetectIntentRequest

    @property
    def responseId(self) -> str:
        return self._responseId

    @responseId.setter
    def responseId(self, responseId: str) -> None:
        if not isinstance(responseId, str):
            raise Exception(f"responseId was type {type(responseId)} which is not valid value for his parameter.")
        self._responseId = responseId

    @property
    def session(self) -> str:
        return self._session

    @session.setter
    def session(self, session: str) -> None:
        if not isinstance(session, str):
            raise Exception(f"session was type {type(session)} which is not valid value for his parameter.")
        self._session = session
