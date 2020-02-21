from abc import abstractmethod
from json import loads as json_loads

from inoft_vocal_framework.platforms_handlers.alexa_v1.session import Session
from inoft_vocal_framework.platforms_handlers.current_platform_data import CurrentPlatformData
from inoft_vocal_framework.platforms_handlers.databases.dynamodb import DynamoDbAdapter
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.platforms_handlers.response_factory import Response
from inoft_vocal_framework.safe_dict import SafeDict

from inoft_vocal_framework.platforms_handlers.alexa_v1.request import Request as RequestAlexa
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request as RequestDialogflow
from inoft_vocal_framework.platforms_handlers.alexa_v1.handler_input import AlexaHandlerInput
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.handler_input import DialogFlowHandlerInput
from inoft_vocal_framework.platforms_handlers.samsungbixby_v1.handler_input import BixbyHandlerInput


class HandlerInput(CurrentPlatformData):
    def __init__(self, db_table_name: str, db_region_name=None):
        self.is_alexa_v1 = False
        self.is_dialogflow_v1 = False
        self.is_bixby_v1 = False

        self.session = Session()
        # self.context = None
        # self.response = Response()

        self._simple_session_user_data = None
        self._persistent_user_id = None
        self._persistent_user_data = None
        self.persistent_attributes_been_modified = False

        self.dynamodb_adapter = DynamoDbAdapter(table_name=db_table_name, region_name=db_region_name,
                                                primary_key_name="id", create_table=True)

        self._alexaHandlerInput, self._dialogFlowHandlerInput, self._bixbyHandlerInput = None, None, None

    @property
    def simple_session_user_data(self) -> SafeDict:
        if self._simple_session_user_data is None:
            if self.is_alexa_v1 is True:
                self._simple_session_user_data = self.alexaHandlerInput.session_attributes
            elif self.is_dialogflow_v1 is True:
                self._simple_session_user_data = self.dialogFlowHandlerInput.simple_session_user_data
            elif self.is_bixby_v1 is True:
                pass

            if not isinstance(self._simple_session_user_data, SafeDict):
                self._simple_session_user_data = SafeDict()
        return self._simple_session_user_data

    @property
    def persistent_user_id(self) -> str:
        if not isinstance(self._persistent_user_id, str) or (self._persistent_user_id.replace(" ", "") == ""):
            if self.is_alexa_v1 is True:
                user_id = SafeDict(self.alexaHandlerInput.session.user).get("userId").to_str(default=None)
            elif self.is_dialogflow_v1 is True:
                user_id = self.dialogFlowHandlerInput.get_user_id()
            elif self.is_bixby_v1 is True:
                user_id = self.bixbyHandlerInput.request.userId

            if not isinstance(user_id, str) or user_id.replace(" ", "") == "":
                from inoft_vocal_framework.utils.general import generate_uuid4
                self._persistent_user_id = generate_uuid4()
                # We need to set the persistent_user_id before memorizing it, because the memorize function will access the
                # persistent_user_data, and if the user_id is not set, we will get stuck in an infinite recursion loop
                self.persistent_memorize("userId", user_id)
                print(f"user_id {self._persistent_user_id} has been memorized in the database.")
            else:
                self._persistent_user_id = user_id

        print(f"_persistent_user_id = {self._persistent_user_id}")
        return self._persistent_user_id

    @property
    def persistent_user_data(self) -> SafeDict:
        if self._persistent_user_data is None:
            persistent_user_data = self.dynamodb_adapter.get_persistent_attributes(user_id=self.persistent_user_id)
            if isinstance(persistent_user_data, dict):
                self._persistent_user_data = SafeDict(persistent_user_data)
            else:
                self._persistent_user_data = SafeDict()

        print(f"_persistent_user_data = {self._persistent_user_data}")
        return self._persistent_user_data

    def load_event_and_context(self, event: dict, context: dict) -> None:
        if self.is_alexa_v1 is True:
            self._alexaHandlerInput = AlexaHandlerInput()
            self.alexaHandlerInput.load_event_and_context(event=event, context=context)

        elif self.is_dialogflow_v1 is True:
            self._dialogFlowHandlerInput = DialogFlowHandlerInput()
            NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self.dialogFlowHandlerInput.request,
                                                                      request_json_dict_or_stringed_dict=event,
                                                                      key_names_identifier_objects_to_go_into=["json_key"])

        elif self.is_bixby_v1 is True:
            self._bixbyHandlerInput = BixbyHandlerInput()
            NestedObjectToDict.process_and_set_json_request_to_object(object_class_to_set_to=self.bixbyHandlerInput.request,
                                                                      request_json_dict_or_stringed_dict=event,
                                                                      key_names_identifier_objects_to_go_into=["json_key"])

    def is_launch_request(self) -> bool:
        if self.is_alexa_v1 is True:
            return self.alexaHandlerInput.request.is_launch_request()
        elif self.is_dialogflow_v1 is True:
            return self.dialogFlowHandlerInput.request.is_launch_request()
        elif self.is_bixby_v1 is True:
            return self.bixbyHandlerInput.request.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        if not isinstance(intent_names_list, list):
            if isinstance(intent_names_list, str):
                intent_names_list = [intent_names_list]
            else:
                raise Exception(f"The intent_names_list must be a list or a str in order to be converted to a list, but it was a {type(intent_names_list)} object : {intent_names_list}")

        if self.is_alexa_v1 is True:
            return self.alexaHandlerInput.request.is_in_intent_names(intent_names_list=intent_names_list)
        elif self.is_dialogflow_v1 is True:
            return self.dialogFlowHandlerInput.request.is_in_intent_names(intent_names_list=intent_names_list)
        elif self.is_bixby_v1 is True:
            return self.bixbyHandlerInput.request.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str) -> None:
        if self.is_alexa_v1 is True:
            self.alexaHandlerInput.response.say(text_or_ssml=text_or_ssml)
        elif self.is_dialogflow_v1 is True:
            self.dialogFlowHandlerInput.response.say(text_or_ssml=text_or_ssml)
        elif self.is_bixby_v1 is True:
            self.bixbyHandlerInput.response.say(text_or_ssml=text_or_ssml)

    def reprompt(self, text_or_ssml: str) -> None:
        if self.is_alexa_v1 is True:
            self.alexaHandlerInput.response.reprompt(text_or_ssml=text_or_ssml)
        elif self.is_dialogflow_v1 is True:
            self.dialogFlowHandlerInput.response.reprompt(text_or_ssml=text_or_ssml)
        elif self.is_bixby_v1 is True:
            self.bixbyHandlerInput.response.reprompt(text_or_ssml=text_or_ssml)

    def get_intent_arg_value(self, arg_key: str):
        if self.is_alexa_v1 is True:
            return self.alexaHandlerInput.request.get_intent_slot_value(slot_key=arg_key)
        elif self.is_dialogflow_v1 is True:
            return self.dialogFlowHandlerInput.request.get_intent_parameter_value(parameter_key=arg_key)
        elif self.is_bixby_v1 is True:
            return self.bixbyHandlerInput.request.get_intent_parameter_value(parameter_key=arg_key)

    def session_memorize(self, data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            self.simple_session_user_data.put(dict_key=data_key, value_to_put=data_value)

    def session_batch_memorize(self, data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                self.simple_session_user_data.put(dict_key=key_item, value_to_put=value_item)

    def session_remember(self, data_key: str, specific_object_type=None):
        data_object = self.simple_session_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    def session_forget(self, data_key: str) -> None:
        self.simple_session_user_data.pop(dict_key=data_key)

    def persistent_memorize(self, data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            self.persistent_attributes_been_modified = True
            self.persistent_user_data.put(dict_key=data_key, value_to_put=data_value)

    def persistent_batch_memorize(self, data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                self.persistent_attributes_been_modified = True
                self.persistent_user_data.put(dict_key=key_item, value_to_put=value_item)

    def persistent_remember(self, data_key: str, specific_object_type=None):
        data_object = self.persistent_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    def persistent_forget(self, data_key: str) -> None:
        self.persistent_attributes_been_modified = True
        self.persistent_user_data.pop(dict_key=data_key)

    def memorize_session_then_state(self, state_handler_class_type_or_name) -> None:
        from inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftStateHandler

        if state_handler_class_type_or_name is not None:
            then_state_class_name = None

            if isinstance(state_handler_class_type_or_name, type):
                try:
                    if InoftStateHandler in state_handler_class_type_or_name.__bases__:
                        then_state_class_name = state_handler_class_type_or_name.__name__
                    else:
                        raise Exception(f"The state handler {state_handler_class_type_or_name} did not had {InoftStateHandler} in its bases classes.")
                except Exception as e:
                    raise Exception(f"Error while setting the following session_then_state {state_handler_class_type_or_name}."
                                    f"Make sure its a class with {InoftStateHandler} as its/one of its parent class."
                                    f"No checks are being made on the class, only a try and except that returned : {e}")

            elif isinstance(state_handler_class_type_or_name, str):
                then_state_class_name = state_handler_class_type_or_name

            if then_state_class_name is not None:
                self.session_memorize(data_key="then_state", data_value=then_state_class_name)
        else:
            raise Exception(f"state_handler_class_type_or_name must be an class type or str but was {state_handler_class_type_or_name}")

    def remember_session_then_state(self):
        last_session_then_state = self.session_remember("then_state", str)
        if last_session_then_state.replace(" ", "") != "":
            return last_session_then_state
        else:
            return None

    def forget_session_then_state(self) -> None:
        self.session_forget("then_state")

    def to_platform_dict(self) -> dict:
        # todo: improve this code, i found it dirty...
        if self.persistent_attributes_been_modified:
            self.dynamodb_adapter.save_attributes(user_id=self.persistent_user_id,
                                                  smart_session_attributes=None,
                                                  persistent_attributes=self.persistent_user_data.to_dict())

        if self.is_alexa_v1 is True:
            return {
                "version": "1.0",
                "sessionAttributes": self.simple_session_user_data.to_dict(),
                "response": self.alexaHandlerInput.response.to_dict()["response"]  # todo: fix the need to enter with response key
            }
        elif self.is_dialogflow_v1 is True:
            self.dialogFlowHandlerInput.response.payload.google.userStorage = str({"userId": self.persistent_user_id})

            from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import OutputContextItem
            session_user_data_context_item = OutputContextItem(session_id=self.dialogFlowHandlerInput.session_id,
                                                               name=OutputContextItem.session_data_name)

            for key_item_saved_data, value_item_saved_data in self.simple_session_user_data.to_dict().items():
                session_user_data_context_item.add_set_session_attribute(key_item_saved_data, value_item_saved_data)
            self.dialogFlowHandlerInput.response.add_output_context_item(session_user_data_context_item)

            return self.dialogFlowHandlerInput.response.to_dict()
        elif self.is_bixby_v1 is True:
            return self.bixbyHandlerInput.response.to_dict()

    @property
    def alexaHandlerInput(self) -> AlexaHandlerInput:
        return self._alexaHandlerInput

    @property
    def dialogFlowHandlerInput(self) -> DialogFlowHandlerInput:
        return self._dialogFlowHandlerInput

    @property
    def bixbyHandlerInput(self) -> BixbyHandlerInput:
        return self._bixbyHandlerInput


class HandlerInputWrapper:
    def __init__(self, parent_handler=None):
        if parent_handler is None:
            self._handler_input = None
        else:
            try:
                self._handler_input = parent_handler.handler_input
            except Exception as e:
                raise Exception(f"A parent_handler has been specified, but do not has an handler_input property : {parent_handler} : {e}")

    @property
    def handler_input(self) -> HandlerInput:
        return self._handler_input

    @handler_input.setter
    def handler_input(self, handler_input: HandlerInput) -> None:
        if not isinstance(handler_input, HandlerInput):
            raise Exception(f"handler_input was type {type(handler_input)} which is not valid value for his parameter.")
        self._handler_input = handler_input

    def is_launch_request(self) -> bool:
        return self.handler_input.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        return self.handler_input.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str):
        self.handler_input.say(text_or_ssml=text_or_ssml)
        return self

    def reprompt(self, text_or_ssml: str):
        self.handler_input.reprompt(text_or_ssml=text_or_ssml)
        return self

    def get_intent_arg_value(self, arg_key: str):
        return self.handler_input.get_intent_arg_value(arg_key=arg_key)

    def session_memorize(self, data_key: str, data_value=None):
        self.handler_input.session_memorize(data_key=data_key, data_value=data_value)
        return self

    def session_batch_memorize(self, data_dict: dict):
        self.handler_input.session_batch_memorize(data_dict=data_dict)
        return self

    def session_remember(self, data_key: str, specific_object_type=None):
        return self.handler_input.session_remember(data_key=data_key, specific_object_type=specific_object_type)

    def session_forget(self, data_key: str) -> None:
        self.handler_input.session_forget(data_key=data_key)
        return self

    def persistent_memorize(self, data_key: str, data_value=None):
        self.handler_input.persistent_memorize(data_key=data_key, data_value=data_value)
        return self

    def persistent_batch_memorize(self, data_dict: dict):
        self.handler_input.persistent_batch_memorize(data_dict=data_dict)
        return self

    def persistent_remember(self, data_key: str, specific_object_type=None):
        return self.handler_input.persistent_remember(data_key=data_key, specific_object_type=specific_object_type)

    def persistent_forget(self, data_key: str):
        self.handler_input.persistent_forget(data_key=data_key)
        return self

    def memorize_session_then_state(self, state_handler_class_type_or_name):
        self.handler_input.memorize_session_then_state(state_handler_class_type_or_name=state_handler_class_type_or_name)
        return self

    def remember_session_then_state(self):
        self.handler_input.remember_session_then_state()
        return self

    def forget_session_then_state(self):
        self.handler_input.forget_session_then_state()

    # todo: add the then states saved in the persistent attributes, allow to
    #  set who should take over if there is a then state in persistent and session

    def to_platform_dict(self) -> dict:
        return self.handler_input.to_platform_dict()

    @property
    def is_alexa_v1(self) -> bool:
        return self.handler_input.is_alexa_v1

    @property
    def is_dialogflow_v1(self) -> bool:
        return self.handler_input.is_dialogflow_v1

    @property
    def is_bixby_v1(self) -> bool:
        return self.handler_input.is_bixby_v1

    @property
    def alexaHandlerInput(self) -> AlexaHandlerInput:
        return self.handler_input.alexaHandlerInput

    @property
    def dialogFlowHandlerInput(self) -> DialogFlowHandlerInput:
        return self.handler_input.dialogFlowHandlerInput

    @property
    def bixbyHandlerInput(self) -> BixbyHandlerInput:
        return self.handler_input.bixbyHandlerInput
