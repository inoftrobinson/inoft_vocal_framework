from json import loads as json_loads

from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.current_platform_static_data import CurrentPlatformData, SessionInfo
from inoft_vocal_framework.platforms_handlers.databases.dynamodb import DynamoDbAdapter
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.platforms_handlers.response_factory import Response
from inoft_vocal_framework.safe_dict import SafeDict

from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request as RequestAlexa
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request as RequestDialogflow
from inoft_vocal_framework.platforms_handlers.alexa_v1.handler_input import AlexaHandlerInput
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.handler_input import DialogFlowHandlerInput


class HandlerInput:
    session = Session()
    context = None
    response = Response()

    session_user_data = SafeDict()
    persistent_user_id = None
    persistent_user_data = SafeDict()
    persistent_attributes_been_modified = False

    dynamodb_adapter = DynamoDbAdapter(table_name="hackaton-cite-des-sciences_users-data", partition_key_name="id", create_table=True)

    @staticmethod
    def load_persistent_user_data() -> None:
        persistent_user_data = HandlerInput.dynamodb_adapter.get_attributes(user_id=HandlerInput.get_user_id())
        print(f"persistent_user_data = {persistent_user_data}")

        if isinstance(persistent_user_data, dict):
            HandlerInput.persistent_user_data = SafeDict(persistent_user_data)
        else:
            HandlerInput.persistent_user_data = SafeDict()

    @staticmethod
    def get_user_id() -> str:
        user_id = None

        if not isinstance(HandlerInput.persistent_user_id, str) or HandlerInput.persistent_user_id.replace(" ", "") == "":
            if CurrentPlatformData.is_alexa_v1 is True:
                user_id = SafeDict(AlexaHandlerInput.session.user).get("userId").to_str(default=None)
            elif CurrentPlatformData.is_dialogflow_v1 is True:
                user_id = DialogFlowHandlerInput.get_user_id()

            if not isinstance(user_id, str) or user_id.replace(" ", "") == "":
                user_id = HandlerInput._generate_memorize_user_id()

            HandlerInput.persistent_user_id = user_id
            HandlerInput.dynamodb_adapter.user_id = HandlerInput.persistent_user_id

        print(f"user_id = {user_id}")
        return user_id

    @staticmethod
    def _generate_memorize_user_id() -> str:
        from uuid import uuid4 as uuid4_generator
        user_id = str(uuid4_generator())
        HandlerInput.persistent_memorize("userId", user_id)
        print(f"Created a new user_id, will now create the field in the database : {user_id}")
        return user_id

    @staticmethod
    def load_event_and_context(event: dict, context: dict):
        if CurrentPlatformData.is_alexa_v1 is True:
            AlexaHandlerInput.load_event_and_context(event=event, context=context)
            HandlerInput.load_persistent_user_data()

        elif CurrentPlatformData.is_dialogflow_v1 is True:
            NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=DialogFlowHandlerInput.request,
                                                                      request_json_dict_or_stringed_dict=event,
                                                                      key_names_identifier_objects_to_go_into=["json_key"])
            HandlerInput.load_persistent_user_data()

            SessionInfo.session_id = DialogFlowHandlerInput.request.session  # Important to set the session id for google assistant

            for output_context in DialogFlowHandlerInput.request.queryResult.outputContexts:
                if isinstance(output_context, dict) and "name" in output_context.keys() and "parameters" in output_context.keys():
                    all_texts_after_slash = output_context["name"].split("/")
                    last_text_after_slash = all_texts_after_slash[len(all_texts_after_slash) - 1]
                    if last_text_after_slash == "session_user_data":
                        parameters_stringed_dict_or_dict = output_context["parameters"]
                        if parameters_stringed_dict_or_dict is not None:
                            if isinstance(parameters_stringed_dict_or_dict, str):
                                parameters_stringed_dict_or_dict = json_loads(parameters_stringed_dict_or_dict)
                            if isinstance(parameters_stringed_dict_or_dict, dict):
                                HandlerInput.session_user_data = SafeDict(parameters_stringed_dict_or_dict)
                            else:
                                raise Exception(f"parameters_stringed_dict_or_dict was nto None, not a str, dict and could not be json converted to a dict : {parameters_stringed_dict_or_dict}")

    @staticmethod
    def is_launch_request():
        if CurrentPlatformData.is_alexa_v1 is True:
            return AlexaHandlerInput.request.is_launch_request()

        elif CurrentPlatformData.is_dialogflow_v1 is True:
            return DialogFlowHandlerInput.request.is_launch_request()

    @staticmethod
    def is_in_intent_names(intent_names_list):
        if not isinstance(intent_names_list, list):
            if isinstance(intent_names_list, str):
                intent_names_list = [intent_names_list]
            else:
                raise Exception(f"The intent_names_list must be a list or a str in order to be converted to a list, but it was a {type(intent_names_list)} object : {intent_names_list}")

        if CurrentPlatformData.is_alexa_v1 is True:
            return AlexaHandlerInput.is_in_intent_names(intent_names_list=intent_names_list)

        elif CurrentPlatformData.is_dialogflow_v1 is True:
            return DialogFlowHandlerInput.request.is_in_intent_names(intent_names_list=intent_names_list)

    @staticmethod
    def say(text_or_ssml: str):
        if CurrentPlatformData.is_alexa_v1 is True:
            AlexaHandlerInput.say(text_or_ssml=text_or_ssml)
        elif CurrentPlatformData.is_dialogflow_v1 is True:
            DialogFlowHandlerInput.say(text_or_ssml=text_or_ssml)

    @staticmethod
    def session_memorize(data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            HandlerInput.session_user_data.put(dict_key=data_key, value_to_put=data_value)

    @staticmethod
    def session_batch_memorize(data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                HandlerInput.session_user_data.put(dict_key=key_item, value_to_put=value_item)

    @staticmethod
    def session_remember(data_key: str, specific_object_type=None):
        data_object = HandlerInput.session_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    @staticmethod
    def persistent_memorize(data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            HandlerInput.persistent_attributes_been_modified = True
            HandlerInput.persistent_user_data.put(dict_key=data_key, value_to_put=data_value)

    @staticmethod
    def persistent_batch_memorize(data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                HandlerInput.persistent_attributes_been_modified = True
                HandlerInput.persistent_user_data.put(dict_key=key_item, value_to_put=value_item)

    @staticmethod
    def persistent_remember(data_key: str, specific_object_type=None):
        data_object = HandlerInput.persistent_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    @staticmethod
    def to_platform_dict():
        HandlerInput.session.attributes = HandlerInput.session_user_data.to_dict()
        # todo: improve this code, i found it dirty...
        if HandlerInput.persistent_attributes_been_modified:
            HandlerInput.dynamodb_adapter.save_attributes(HandlerInput.persistent_user_data.to_dict())

        if CurrentPlatformData.is_alexa_v1 is True:
            return {
                "version": "1.0",
                "sessionAttributes": HandlerInput.session.attributes,
                "response": AlexaHandlerInput.response.to_dict()["response"]  # todo: fix the need to enter with response key
            }
        elif CurrentPlatformData.is_dialogflow_v1 is True:
            return DialogFlowHandlerInput.response.to_dict()
