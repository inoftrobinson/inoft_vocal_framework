import logging
from collections import Callable
from typing import Optional, Any

from inoft_vocal_framework.audio_editing.audioclip import AudioBlock
from inoft_vocal_framework.dummy_object import DummyObject
from inoft_vocal_framework.platforms_handlers.current_used_platform_info import CurrentUsedPlatformInfo
from inoft_vocal_framework.databases.dynamodb.dynamodb import DynamoDbAttributesAdapter, DynamoDbNotificationsSubscribers
from inoft_vocal_framework.platforms_handlers.notifications_subscribers import NotificationsSubscribers
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.skill_settings.skill_settings import Settings
from inoft_vocal_framework.user_data.user_data import UserData


class HandlerInput(CurrentUsedPlatformInfo):
    def __init__(self, settings_instance: Settings, use_default_settings_if_missing: bool = False):
        super().__init__()
        self._use_default_settings_if_missing = use_default_settings_if_missing

        self.settings = settings_instance

        if self.settings.database_sessions_users_data.db_table_name is None:
            # If the table_name has not been found, we disable the database (yet we do not raise, since
            # in some cases, it could be normal to not specify a table_name, for example for our unit tests)
            self.settings.database_sessions_users_data.disable_database = True

        self._session_id = None
        self._is_invocation_new_session = None
        self._default_session_data_timeout = self.settings.default_session_data_timeout
        self._session_been_resumed = None
        self._simple_session_user_data = None
        self._smart_session_user_data = None
        self._persistent_user_id = None
        self._persistent_user_data = None
        self._interactivity_callback_functions = None
        self.data_for_database_has_been_modified = False

        self._is_option_select_request = None
        self._selected_option_identifier = None

        self.__attributes_dynamodb_adapter = None
        self.__notifications_subscribers_dynamodb_adapter = None

        self._notifications_subscribers = None
        self._alexaHandlerInput, self._dialogFlowHandlerInput, self._bixbyHandlerInput, self._discordHandlerInput = None, None, None, None

        self._user_data = None

    @property
    def _settings(self) -> Settings:
        if self.__settings is None:
            self.__settings = Settings()
        return self.__settings

    @property
    def _attributes_dynamodb_adapter(self) -> DynamoDbAttributesAdapter:
        if self.__attributes_dynamodb_adapter is None:
            if self.settings.database_sessions_users_data.disable_database is False:
                self.__attributes_dynamodb_adapter = DynamoDbAttributesAdapter(
                    table_name=self.settings.database_sessions_users_data.db_table_name,
                    region_name=self.settings.database_sessions_users_data.db_region_name,
                    primary_key_name="id", create_table=True)
        return self.__attributes_dynamodb_adapter

    @property
    def _notifications_subscribers_dynamodb_adapter(self) -> DynamoDbNotificationsSubscribers:
        if self.__notifications_subscribers_dynamodb_adapter is None:
            def raise_exception_parameter_missing(parameter_name: str):
                # todo: add docs link
                raise Exception(f"The {parameter_name} setting has not been found in the user_notifications_subscriptions "
                                f"section in your app_settings file.\nPlease refer to the documentation to see the format "
                                f"and parameters of the user_notifications_subscriptions setting.")

            self.__notifications_subscribers_dynamodb_adapter = DynamoDbNotificationsSubscribers(
                table_name=self.settings.database_users_notifications_subscriptions.db_table_name,
                region_name=self.settings.database_users_notifications_subscriptions.db_region_name,
                create_table=True)

        return self.__notifications_subscribers_dynamodb_adapter


    @property
    def session_id(self):
        if self._session_id is None:
            if self.is_alexa is True:
                self._session_id = self.alexaHandlerInput.session.sessionId
            elif self.is_dialogflow is True:
                self._session_id = self.dialogFlowHandlerInput.session_id
            elif self.is_bixby is True:
                self._session_id = self.bixbyHandlerInput.request.context.sessionId

            if not isinstance(self._session_id, str):
                self._session_id = str(self._session_id)

        return self._session_id

    @property
    def is_invocation_new_session(self) -> bool:
        if self._is_invocation_new_session is None:
            if self.is_alexa is True:
                self._is_invocation_new_session = self.alexaHandlerInput.is_new_session
            elif self.is_dialogflow is True:
                self._is_invocation_new_session = self.dialogFlowHandlerInput.is_new_session
            elif self.is_bixby is True:
                last_session_id = self.persistent_remember("lastSessionId", str)
                if last_session_id is None or last_session_id == "":
                    self._is_invocation_new_session = True
                elif self.bixbyHandlerInput.context.sessionId != last_session_id:
                    self._is_invocation_new_session = True
        return self._is_invocation_new_session

    @property
    def default_session_data_timeout(self):
        return self._default_session_data_timeout

    # todo: allow for the session timeout to be personallized and memorized for every user
    @default_session_data_timeout.setter
    def default_session_data_timeout(self, default_session_data_timeout) -> None:
        if default_session_data_timeout is not None and not isinstance(default_session_data_timeout, int):
            raise Exception(f"The default_session_data_timeout variable must be of type {None} or {int} but was : {default_session_data_timeout}")
        self._default_session_data_timeout = default_session_data_timeout

    @property
    def session_been_resumed(self) -> bool:
        if self._session_been_resumed is None:
            self._load_smart_session_user_data()
        return self._session_been_resumed

    @property
    def simple_session_user_data(self) -> SafeDict:
        if self._simple_session_user_data is None:
            if self.is_alexa is True:
                self._simple_session_user_data = self.alexaHandlerInput.session_attributes
            elif self.is_dialogflow is True:
                self._simple_session_user_data = self.dialogFlowHandlerInput.simple_session_user_data
            elif self.is_bixby is True:
                print("simple_session_user_data is not implemented for the bixby platform.")

            if not isinstance(self._simple_session_user_data, SafeDict):
                self._simple_session_user_data = SafeDict()
        return self._simple_session_user_data

    @property
    def user_data(self) -> UserData:
        return self._user_data

    @property
    def smart_session_user_data(self) -> SafeDict:
        return DummyObject()
        if self._smart_session_user_data is None:
            self._load_smart_session_user_data()
        return self._smart_session_user_data

    def _load_smart_session_user_data(self):
        return DummyObject()
        # todo: re-activate that
        """
        # We use a separate function to load the smart session user data, and we do not include it in the property itself,
        # because this function can be called by the smart_session_user_data property or the session_been_resumed property.
        if self._smart_session_user_data is None:
            if self.database_sessions_users_data_disable_database is False:
                self._smart_session_user_data, self._session_been_resumed = self._attributes_dynamodb_adapter.get_smart_session_attributes(
                    user_id=self.persistent_user_id, session_id=self.session_id, timeout_seconds=self.default_session_data_timeout)

                if not isinstance(self._smart_session_user_data, SafeDict):
                    self._smart_session_user_data = SafeDict()
            else:
                self._smart_session_user_data = SafeDict()
        logging.debug(f"_smart_session_user_data = {self._smart_session_user_data}")
        """

    @property
    def persistent_user_id(self) -> str:
        if not isinstance(self._persistent_user_id, str) or (self._persistent_user_id.replace(" ", "") == ""):
            user_id: Optional[str] = None
            if self.is_alexa is True:
                user_id = SafeDict(self.alexaHandlerInput.session.user).get('userId').to_str(default=None)
            elif self.is_dialogflow is True:
                user_id = self.dialogFlowHandlerInput.get_user_id()
            elif self.is_bixby is True:
                user_id = self.bixbyHandlerInput.request.context.userId
            elif self.is_discord is True:
                user_id = self.discordHandlerInput.request.author.id

            if user_id is None or not isinstance(user_id, str) or user_id.replace(" ", "") == "":
                from inoft_vocal_framework.utils.general import generate_uuid4
                self._persistent_user_id = generate_uuid4()
                # We need to set the persistent_user_id before memorizing it, because the memorize function will access the
                # persistent_user_data, and if the user_id is not set, we will get stuck in an infinite recursion loop
                self.persistent_memorize("userId", user_id)
                print(f"user_id {self._persistent_user_id} has been memorized in the database.")
            else:
                self._persistent_user_id = user_id
            logging.debug(f"_persistent_user_id = {self._persistent_user_id}")
        return self._persistent_user_id

    @property
    def persistent_user_data(self) -> SafeDict:
        if self._persistent_user_data is None:
            if self.database_sessions_users_data_disable_database is False:
                self._persistent_user_data = self._attributes_dynamodb_adapter.get_persistent_attributes(user_id=self.persistent_user_id)
            if not isinstance(self._persistent_user_data, SafeDict):
                self._persistent_user_data = SafeDict()
            logging.debug(f"_persistent_user_data = {self._persistent_user_data}")
        return self._persistent_user_data

    @property
    def interactivity_callback_functions(self) -> SafeDict:
        if self._interactivity_callback_functions is None:
            self._interactivity_callback_functions = self.smart_session_user_data.get("interactivityCallbackFunctions").to_safedict()
        return self._interactivity_callback_functions

    def load_event(self, event: dict) -> None:
        if self.is_alexa is True:
            from inoft_vocal_framework.platforms_handlers.alexa.handler_input import AlexaHandlerInput
            self._alexaHandlerInput = AlexaHandlerInput(parent_handler_input=self, **event)

        elif self.is_dialogflow is True:
            from inoft_vocal_framework.platforms_handlers.dialogflow.handler_input import DialogFlowHandlerInput
            self._dialogFlowHandlerInput = DialogFlowHandlerInput(parent_handler_input=self, request=event)

        elif self.is_bixby is True:
            from inoft_vocal_framework.platforms_handlers.samsungbixby import BixbyHandlerInput
            self._bixbyHandlerInput = BixbyHandlerInput(parent_handler_input=self)

            NestedObjectToDict.process_and_set_json_to_object(
                object_class_to_set_to=self.bixbyHandlerInput.request.context,
                request_json_dict_stringed_dict_or_list=event["context"],
                key_names_identifier_objects_to_go_into=["json_key"]
            )
            NestedObjectToDict.process_and_set_json_to_object(
                object_class_to_set_to=self.bixbyHandlerInput.request,
                request_json_dict_stringed_dict_or_list=event["parameters"],
                key_names_identifier_objects_to_go_into=["json_key"]
            )

        elif self.is_discord is True:
            from inoft_vocal_framework.platforms_handlers.discord.handler_input import DiscordHandlerInput
            from discord import Message
            event: Message
            self._discordHandlerInput = DiscordHandlerInput(parent_handler_input=self, request=event)

    def _force_load_alexa(self):
        self.set_platform_to_alexa()
        from inoft_vocal_framework.platforms_handlers.alexa.handler_input import AlexaHandlerInput
        self._alexaHandlerInput = AlexaHandlerInput(parent_handler_input=self)

    def _force_load_dialogflow(self):
        self.set_platform_to_dialogflow()
        from inoft_vocal_framework.platforms_handlers.dialogflow import DialogFlowHandlerInput
        self._dialogFlowHandlerInput = DialogFlowHandlerInput(parent_handler_input=self)

    def _force_load_bixby(self):
        self.set_platform_to_bixby()
        from inoft_vocal_framework.platforms_handlers.samsungbixby import BixbyHandlerInput
        self._bixbyHandlerInput = BixbyHandlerInput(parent_handler_input=self)

    def _force_load_discord(self):
        self.set_platform_to_discord()
        from inoft_vocal_framework.platforms_handlers.discord.handler_input import DiscordHandlerInput
        self._discordHandlerInput = DiscordHandlerInput(parent_handler_input=self)

    def save_callback_function_to_database(self, callback_functions_key_name: str, callback_function: Callable, identifier_key: Optional[str] = None):
        # todo: fix bug where the identifier_key is not the right now if it has been modified because there were only 1 element
        # No matter if we already have functions for the different ids in the same key name, we remember the dict of all the
        # callback functions of the key name (will be an empty dict if was not present), then we add the callback for the
        # current specified identifier. Finally, we can memorize this new updated list.
        callback_functions_dict: Optional[dict] = self.user_data.get_field(field_path=callback_functions_key_name)
        from inspect import getfile

        item_dict = {
            'file_filepath_containing_callback': getfile(callback_function),
            'callback_function_path': callback_function.__qualname__
        }

        if identifier_key is not None:
            callback_functions_dict[identifier_key] = item_dict
        else:
            callback_functions_dict = item_dict

        self.session_memorize(callback_functions_key_name, callback_functions_dict)

    def need_to_be_handled_by_callback(self) -> bool:
        if self._is_option_select_request is None:
            if self.is_alexa is True:
                return False
            elif self.is_dialogflow is True:
                self._is_option_select_request = self.dialogFlowHandlerInput.is_option_select_request()
            elif self.is_bixby is True:
                return False
        return self._is_option_select_request

    @property
    def selected_option_identifier(self) -> str:
        if self.is_alexa:
            raise
        elif self.is_dialogflow is True:
            self._selected_option_identifier = self.dialogFlowHandlerInput.selected_option_identifier()
        elif self.is_bixby:
            raise
        return self._selected_option_identifier

    def is_launch_request(self) -> bool:
        if self.is_alexa is True:
            return self.alexaHandlerInput.is_launch_request()
        elif self.is_dialogflow is True:
            return self.dialogFlowHandlerInput.is_launch_request()
        elif self.is_bixby is True:
            return self.bixbyHandlerInput.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        if self.is_alexa is True:
            return self.alexaHandlerInput.is_in_intent_names(intent_names_list=intent_names_list)
        elif self.is_dialogflow is True:
            return self.dialogFlowHandlerInput.is_in_intent_names(intent_names_list=intent_names_list)
        elif self.is_bixby is True:
            return self.bixbyHandlerInput.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str) -> None:
        if self.is_alexa is True:
            self.alexaHandlerInput.say(text_or_ssml=text_or_ssml)
        elif self.is_dialogflow is True:
            self.dialogFlowHandlerInput.say(text_or_ssml=text_or_ssml)
        elif self.is_bixby is True:
            self.bixbyHandlerInput.say(text_or_ssml=text_or_ssml)
        elif self.is_discord is True:
            self.discordHandlerInput.say(text_or_ssml=text_or_ssml)

    def say_ssml(self, ssml: str) -> None:
        if self.is_alexa is True:
            self.alexaHandlerInput.say_ssml(ssml=ssml)
        elif self.is_dialogflow is True:
            raise Exception("Not implemented")
        elif self.is_bixby is True:
            raise Exception("Not implemented")
        elif self.is_discord is True:
            raise Exception("Not implemented")

    def reprompt(self, text_or_ssml: str) -> None:
        if self.is_alexa is True:
            self.alexaHandlerInput.reprompt(text_or_ssml=text_or_ssml)
        elif self.is_dialogflow is True:
            self.dialogFlowHandlerInput.reprompt(text_or_ssml=text_or_ssml)
        elif self.is_bixby is True:
            self.bixbyHandlerInput.reprompt(text_or_ssml=text_or_ssml)

    def end_session(self, should_end: bool = True) -> None:
        if self.is_alexa is True:
            self.alexaHandlerInput.end_session(should_end=should_end)
        elif self.is_dialogflow is True:
            self.dialogFlowHandlerInput.response.end_session(should_end=should_end)
        elif self.is_bixby is True:
            raise

    def get_intent_arg_value(self, arg_key: str):
        if self.is_alexa is True:
            return self.alexaHandlerInput.request.get_intent_slot_value(slot_key=arg_key)
        elif self.is_dialogflow is True:
            return self.dialogFlowHandlerInput.request.get_intent_parameter_value(parameter_key=arg_key)
        elif self.is_bixby is True:
            return self.bixbyHandlerInput.request.get_intent_parameter_value(parameter_key=arg_key)

    def simple_session_memorize(self, data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            self.simple_session_user_data.put(dict_key=data_key, value_to_put=data_value)

    def simple_session_batch_memorize(self, data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                self.simple_session_user_data.put(dict_key=key_item, value_to_put=value_item)

    def simple_session_remember(self, data_key: str, specific_object_type=None):
        data_object = self.simple_session_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    def simple_session_forget(self, data_key: str) -> None:
        self.simple_session_user_data.pop(dict_key=data_key)

    def session_memorize(self, data_key: str, data_value: Any, query_kwargs: Optional[dict] = None) -> bool:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            self.data_for_database_has_been_modified = True
            return self.user_data.update_field(field_path=data_key, value_to_set=data_value, query_kwargs=query_kwargs)
        return False

    def session_batch_memorize(self, data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            if len(data_dict) > 0:
                self.data_for_database_has_been_modified = True

            for key_item, value_item in data_dict.items():
                self.smart_session_user_data.put(dict_key=key_item, value_to_put=value_item)

    def session_remember(self, data_key: str, specific_object_type=None):
        # todo: re-activate that
        return DummyObject()

        data_object = self.smart_session_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    def session_forget(self, data_key: str) -> None:
        self.data_for_database_has_been_modified = True
        self.smart_session_user_data.pop(dict_key=data_key)

    def persistent_memorize(self, data_key: str, data_value=None) -> None:
        if data_value is not None and isinstance(data_key, str) and data_key != "":
            self.data_for_database_has_been_modified = True
            self.persistent_user_data.put(dict_key=data_key, value_to_put=data_value)

    def persistent_batch_memorize(self, data_dict: dict) -> None:
        if not isinstance(data_dict, dict):
            raise Exception(f"The data_dict must be of type dict but was of type {type(data_dict)}")
        else:
            for key_item, value_item in data_dict.items():
                self.data_for_database_has_been_modified = True
                self.persistent_user_data.put(dict_key=key_item, value_to_put=value_item)

    def persistent_remember(self, data_key: str, specific_object_type=None):
        data_object = self.persistent_user_data.get(data_key)
        if specific_object_type is None:
            return data_object.to_any()
        else:
            return data_object.to_specific_type(type_to_return=specific_object_type)

    def persistent_forget(self, data_key: str) -> None:
        self.data_for_database_has_been_modified = True
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

            if isinstance(state_handler_class_type_or_name, str):
                then_state_class_name = state_handler_class_type_or_name

            if then_state_class_name is not None:
                self.session_memorize(data_key='thenState', data_value=then_state_class_name)
        else:
            raise Exception(f"state_handler_class_type_or_name must be an class type or str but was {state_handler_class_type_or_name}")

    def remember_session_then_state(self):
        last_session_then_state: Optional[str] = self.user_data.get_field(field_path='thenState')
        if last_session_then_state is not None and last_session_then_state.replace(" ", "") != "":
            return last_session_then_state
        else:
            return None

    def forget_session_then_state(self) -> bool:
        return self.user_data.delete_field(field_path='thenState')

    def play_audio_block(self, audio_block: AudioBlock) -> bool:
        if self.is_alexa is True:
            return self.alexaHandlerInput.play_audio_block(audio_block=audio_block)
        return False

    def memorize_session_last_intent_handler(self, handler_class_type_instance_name) -> None:
        from inoft_vocal_framework.skill_builder.inoft_skill_builder import InoftRequestHandler, InoftStateHandler

        if handler_class_type_instance_name is not None:
            handler_class_name = None

            if isinstance(handler_class_type_instance_name, str):
                handler_class_name = handler_class_type_instance_name
            else:
                try:
                    handler_class_type_object = handler_class_type_instance_name if callable(handler_class_type_instance_name) else handler_class_type_instance_name.__class__
                    if InoftRequestHandler in handler_class_type_object.__bases__ or InoftStateHandler in handler_class_type_object.__bases__:
                        handler_class_name = handler_class_type_object.__name__
                    else:
                        raise Exception(f"The state handler {handler_class_type_object} did not had {InoftStateHandler} in its bases classes.")
                except Exception as e:
                    raise Exception(f"Error while setting the following session_last_intent_handler {handler_class_type_instance_name}."
                                    f"Make sure its a class with {InoftStateHandler} as its/one of its parent class."
                                    f"No checks are being made on the class, only a try and except that returned : {e}")

            if handler_class_name is not None:
                self.session_memorize(data_key="lastIntentHandler", data_value=handler_class_name)
                print("SAVED")
        else:
            raise Exception(f"handler_class_type_or_name must be an class type or str but was {handler_class_type_instance_name}")

    def remember_session_last_intent_handler(self) -> Optional[str]:
        last_intent_handler_class_name: Optional[str] = self.user_data.get_field(field_path='lastIntentHandler')
        if last_intent_handler_class_name is not None and last_intent_handler_class_name.replace(" ", "") != "":
            return last_intent_handler_class_name
        else:
            return None

    def forget_session_last_intent_handler(self) -> None:
        self.session_forget("lastIntentHandler")

    def save_attributes_if_need_to(self):
        self.user_data.table.commit_operations()

        # todo: deprecate code bellow and the entire attributes_dynamodb_adapter
        if self.data_for_database_has_been_modified is True:
            if self.settings.database_sessions_users_data.disable_database is not True:
                self._attributes_dynamodb_adapter.save_attributes(
                    user_id=self.persistent_user_id, session_id=self.session_id,
                    smart_session_attributes=self.smart_session_user_data.to_dict(),
                    persistent_attributes=self.persistent_user_data.to_dict()
                )

    def _alexa_to_platform_dict(self) -> dict:
        return {
            "version": "1.0",
            "sessionAttributes": self.simple_session_user_data.to_dict(),
            "response": self.alexaHandlerInput._response.to_dict()
        }

    def _dialogflow_to_platform_dict(self) -> dict:
        data_dict_to_store = {'userId': self.persistent_user_id}
        updates_user_id = self.dialogFlowHandlerInput.get_updates_user_id()
        if updates_user_id is not None:
            data_dict_to_store['updatesUserId'] = updates_user_id

        self.dialogFlowHandlerInput._response.payload.google.userStorage = str(data_dict_to_store)

        from inoft_vocal_framework.platforms_handlers.dialogflow.response import OutputContextItem
        session_user_data_context_item = OutputContextItem(
            session_id=self.dialogFlowHandlerInput.session_id,
            name=OutputContextItem.session_data_name
        )

        for key_item_saved_data, value_item_saved_data in self.simple_session_user_data.to_dict().items():
            session_user_data_context_item.add_set_session_attribute(key_item_saved_data, value_item_saved_data)
        self.dialogFlowHandlerInput._response.add_output_context_item(session_user_data_context_item)

        return self.dialogFlowHandlerInput._response.to_dict()

    def _bixby_to_platform_dict(self) -> dict:
        return self.bixbyHandlerInput.response.to_dict()

    def _discord_to_platform_dict(self):
        return None

    def to_platform_dict(self) -> dict:
        switch = {
            self.PLATFORM_KEY_ALEXA: self._alexa_to_platform_dict,
            self.PLATFORM_KEY_DIALOGFLOW: self._dialogflow_to_platform_dict,
            self.PLATFORM_KEY_BIXBY: self._bixby_to_platform_dict,
            self.PLATFORM_KEY_DISCORD: self._discord_to_platform_dict
        }
        handler = switch.get(self.platform, None)
        if handler is None:
            raise Exception(f"Platform not supported : {self.platform}")
        return handler()

    @property
    def notifications_subscribers(self) -> NotificationsSubscribers:
        if self._notifications_subscribers is None:
            self._notifications_subscribers = NotificationsSubscribers(parent_handler_input=self)
        return self._notifications_subscribers

    @property
    def alexaHandlerInput(self):
        return self._alexaHandlerInput if self._alexaHandlerInput is not None else DummyObject()

    @property
    def alexa(self):
        return self.alexaHandlerInput

    @property
    def dialogFlowHandlerInput(self):
        return self._dialogFlowHandlerInput if self._dialogFlowHandlerInput is not None else DummyObject()

    @property
    def google(self):
        return self.dialogFlowHandlerInput

    @property
    def bixbyHandlerInput(self):
        return self._bixbyHandlerInput if self._bixbyHandlerInput is not None else DummyObject()

    @property
    def bixby(self):
        return self.bixbyHandlerInput

    @property
    def discordHandlerInput(self):
        return self._discordHandlerInput if self._discordHandlerInput is not None else DummyObject()

    @property
    def discord(self):
        return self.discordHandlerInput


class HandlerInputWrapper:
    from inoft_vocal_framework.platforms_handlers.dialogflow.handler_input import DialogFlowHandlerInput
    from inoft_vocal_framework.platforms_handlers.alexa.handler_input import AlexaHandlerInput
    from inoft_vocal_framework.platforms_handlers.samsungbixby.handler_input import BixbyHandlerInput

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

    @property
    def session_been_resumed(self):
        return self.handler_input.session_been_resumed

    def is_launch_request(self) -> bool:
        return self.handler_input.is_launch_request()

    def is_in_intent_names(self, intent_names_list) -> bool:
        return self.handler_input.is_in_intent_names(intent_names_list=intent_names_list)

    def say(self, text_or_ssml: str):
        self.handler_input.say(text_or_ssml=text_or_ssml)
        return self

    def say_ssml(self, ssml: str):
        self.handler_input.say_ssml(ssml=ssml)
        return self

    def reprompt(self, text_or_ssml: str):
        self.handler_input.reprompt(text_or_ssml=text_or_ssml)
        return self

    def get_intent_arg_value(self, arg_key: str) -> SafeDict:
        return self.handler_input.get_intent_arg_value(arg_key=arg_key)

    def simple_session_memorize(self, data_key: str, data_value=None):
        self.handler_input.simple_session_memorize(data_key=data_key, data_value=data_value)
        return self

    def end_session(self, should_end: bool = True):
        self.handler_input.end_session(should_end=should_end)
        return self

    def simple_session_batch_memorize(self, data_dict: dict):
        self.handler_input.simple_session_batch_memorize(data_dict=data_dict)
        return self

    def simple_session_remember(self, data_key: str, specific_object_type=None):
        return self.handler_input.simple_session_remember(data_key=data_key, specific_object_type=specific_object_type)

    def simple_session_forget(self, data_key: str):
        self.handler_input.simple_session_forget(data_key=data_key)
        return self

    def session_memorize(self, data_key: str, data_value=None):
        self.handler_input.session_memorize(data_key=data_key, data_value=data_value)
        return self

    def session_batch_memorize(self, data_dict: dict):
        self.handler_input.session_batch_memorize(data_dict=data_dict)
        return self

    def session_remember(self, data_key: str, specific_object_type=None):
        return self.handler_input.session_remember(data_key=data_key, specific_object_type=specific_object_type)

    def session_forget(self, data_key: str):
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

    def play_audio_block(self, audio_block: AudioBlock) -> bool:
        return self.handler_input.play_audio_block(audio_block=audio_block)

    def to_platform_dict(self) -> dict:
        return self.handler_input.to_platform_dict()

    @property
    def is_alexa(self) -> bool:
        return self.handler_input.is_alexa

    @property
    def is_dialogflow(self) -> bool:
        return self.handler_input.is_dialogflow

    @property
    def is_bixby(self) -> bool:
        return self.handler_input.is_bixby

    def is_discord(self) -> bool:
        return self.handler_input.is_discord

    @property
    def alexa(self) -> AlexaHandlerInput:
        return self.handler_input.alexaHandlerInput

    @property
    def google(self) -> DialogFlowHandlerInput:
        return self.handler_input.dialogFlowHandlerInput

    @property
    def bixby(self) -> BixbyHandlerInput:
        return self.handler_input.bixbyHandlerInput

    @property
    def discord(self):
        return self.handler_input.discordHandlerInput
