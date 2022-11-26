import json
import logging
from abc import abstractmethod
from json import dumps as json_dumps

from typing import List, Callable, Any, Optional

from inoft_vocal_framework.dummy_object import DummyObject
from inoft_vocal_framework.exceptions import raise_if_value_not_in_list, raise_if_variable_not_expected_type
from inoft_vocal_framework.platforms_handlers.endpoints_providers.providers import LambdaResponseWrapper
from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput, HandlerInputWrapper
from inoft_vocal_framework.plugins.loader import plugins_load

# todo: Add a prod and dev production mode, so that optisionnal status (like loading of plugins) is done only in developpement

# todo: Add a class with only a CanHandle function (for cases like the Yes and No classical handlers=
from inoft_vocal_framework.skill_settings.skill_settings import Settings


def canProcessIntentNames(intents_names: List[str]):
    print(intents_names)
    # todo: finish the canProcessIntentNames
    def decorator(class_instance: Any):
        """def wrapper(*args, **kwargs):
            return None
        wrapper()"""
        try:
            class_instance_bases = class_instance.__bases__
            if InoftStateHandler in class_instance_bases:
                print("should add state handler to skill switch")
            elif InoftRequestHandler in class_instance_bases:
                print("should add request handler to skill switch")
            # return wrapper
        except Exception as e:
            print(e)
        finally:
            return class_instance
    return decorator

class InoftCondition(HandlerInputWrapper):
    @abstractmethod
    def can_handle(self) -> bool:
        """ Returns true if Request Handler can handle the Request inside Handler Input.
        :return: Boolean value that tells the dispatcher if the current request can be handled by this handler.
        :rtype: bool
        """
        raise NotImplementedError

class InoftHandler(HandlerInputWrapper):
    @abstractmethod
    def handle(self) -> dict:
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def handle_resume(self) -> dict:
        # todo: make the handle resume function functionnal for the handler (cannot use a chain, but need to
        # use a class path, that will be saved in the database)
        print(f"Resuming an user session, but no logic has been found in the handle_resume function, defaulting to the handle function")

class InoftRequestHandler(HandlerInputWrapper):
    @abstractmethod
    def can_handle(self) -> bool:
        """ Returns true if Request Handler can handle the Request inside Handler Input.
        :return: Boolean value that tells the dispatcher if the current request can be handled by this handler.
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self) -> dict:
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def handle_resume(self) -> dict:
        print(f"Resuming an user session, but no logic has been found in the handle_resume function, defaulting to the handle function")

class InoftStateHandler(HandlerInputWrapper):
    # todo: make it possible for a state or request handler to be a nested class inside another one
    @abstractmethod
    def handle(self) -> dict:
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def fallback(self) -> dict:
        """ Handler if no response has been gotten from the handle method.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        return self.handle()

    @abstractmethod
    def handle_resume(self):
        print(f"Resuming an user session, but no logic has been found in the handle_resume function, defaulting to the handle function")

class InoftDefaultFallback(HandlerInputWrapper):
    @abstractmethod
    def handle(self) -> dict:
        raise NotImplementedError

class InoftHandlersGroup:
    @abstractmethod
    def __getattr__(self, item):
        self_vars = vars(self)
        if item in self_vars:
            return self_vars[item]
        else:
            return DummyObject()

    def handle(self) -> dict:
        for var_key, var_object in vars(self).items():
            if InoftRequestHandler in list(var_object.__class__.__bases__):
                if var_object.can_handle() is True:
                    handler_output = var_object.handle()
                    if handler_output is not None:
                        return handler_output


class InoftSkill:
    APP_SETTINGS: Settings

    def __init__(self, settings_instance: Settings = None):
        self.settings = settings_instance
        self.plugins = plugins_load(settings=self.settings)
        # todo: reactivate plugins
        InoftSkill.APP_SETTINGS = self.settings

        self._request_handlers_chain = dict()
        self._state_handlers_chain = dict()
        self._default_fallback_handler = None
        self._handler_input = HandlerInput(settings_instance=settings_instance)

        self.on_interaction_start: List[Callable[[], Any]] = []
        self.on_interaction_end: List[Callable[[], Any]] = []

        self.settings.user_data_plugin.register_plugin(skill=self)
        # todo: add better plugin registration system

    @property
    def settings(self) -> Settings:
        return self._settings

    @settings.setter
    def settings(self, settings: Settings) -> None:
        raise_if_variable_not_expected_type(value=settings, expected_type=Settings, variable_name="settings")
        self._settings = settings

    def add_request_handler(self, request_handler_instance_or_class) -> None:
        if request_handler_instance_or_class is not None:
            try:
                if isinstance(request_handler_instance_or_class, type):
                    # If the variable is a class object we create an instance of the class
                    handler_bases_parent_classes = request_handler_instance_or_class.__bases__
                    request_handler_instance_or_class = request_handler_instance_or_class()
                else:
                    # If the variable is a class instance
                    handler_bases_parent_classes = request_handler_instance_or_class.__class__.__bases__

                if InoftRequestHandler in handler_bases_parent_classes:
                    request_handler_instance_or_class.handler_input = self.handler_input
                    # We set a reference to the skill handler_input in each handler so that it can use it with its HandlerInputWrapper
                    self.request_handlers_chain[request_handler_instance_or_class.__class__.__name__] = request_handler_instance_or_class
            except Exception as e:
                raise Exception(f"Error while adding a request handler. Please make sure it is a {InoftRequestHandler} class object : {e}")
        else:
            raise Exception(f"The following request handler is not a valid handler or do not have "
                            f"{InoftRequestHandler.__name__} as its MetaClass : {request_handler_instance_or_class}")

    def add_state_handler(self, state_handler_instance_or_class) -> None:
        if state_handler_instance_or_class is not None:
            try:
                if isinstance(state_handler_instance_or_class, type):
                    # If the variable is a class object we create an instance of the class
                    handler_bases_parent_classes = state_handler_instance_or_class.__bases__
                    state_handler_instance_or_class = state_handler_instance_or_class()
                else:
                    # If the variable is a class instance
                    handler_bases_parent_classes = state_handler_instance_or_class.__class__.__bases__

                if InoftStateHandler in handler_bases_parent_classes:
                    state_handler_instance_or_class.handler_input = self.handler_input
                    # We set a reference to the skill handler_input in each handler so that it can use it with its HandlerInputWrapper
                    self.state_handlers_chain[state_handler_instance_or_class.__class__.__name__] = state_handler_instance_or_class
            except Exception as e:
                raise Exception(f"Error while adding a state handler. Please make sure it is a {InoftStateHandler} class object : {e}")
        else:
            raise Exception(f"The following state handler is not a valid handler or do not have "
                            f"{InoftStateHandler.__name__} as its MetaClass : {state_handler_instance_or_class}")

    def set_default_fallback_handler(self, default_fallback_handler_instance_or_class) -> None:
        if default_fallback_handler_instance_or_class is not None:
            try:
                if isinstance(default_fallback_handler_instance_or_class, type):
                    # If the variable is a class object we create an instance of the class
                    handler_bases_parent_classes = default_fallback_handler_instance_or_class.__bases__
                    default_fallback_handler_instance_or_class = default_fallback_handler_instance_or_class()
                else:
                    # If the variable is a class instance
                    handler_bases_parent_classes = default_fallback_handler_instance_or_class.__class__.__bases__

                if InoftDefaultFallback in handler_bases_parent_classes:
                    default_fallback_handler_instance_or_class.handler_input = self.handler_input
                    # We set a reference to the skill handler_input in each handler so that it can use it with its HandlerInputWrapper
                    self.default_fallback_handler = default_fallback_handler_instance_or_class
            except Exception as e:
                raise Exception(f"Error while adding a request handler. Please make sure it is a {InoftDefaultFallback} class object : {e}")
        else:
            raise Exception(f"The following fallback handler is not a valid handler or do not have "
                            f"{InoftDefaultFallback.__name__} as its MetaClass : {default_fallback_handler_instance_or_class}")

    def process_request(self):
        output_event = None
        handler_to_use = None
        handler_is_an_alone_callback_function = False
        handler_is_an_audioplayer_handlers_group = False
        handler_is_a_then_state_handler = False
        handler_is_a_request_handler = False

        # If an UPDATES_USER_ID has been found on the Google Assistant Platform, we saved it in the user data.
        if self.handler_input.is_dialogflow is True:
            current_updates_user_id = self.handler_input.dialogFlowHandlerInput.request.get_updates_user_id_if_present()
            if current_updates_user_id is not None:
                remembered_updates_user_id = self.handler_input.persistent_remember("updatesUserId", str)
                if current_updates_user_id != remembered_updates_user_id:
                    self.handler_input.persistent_memorize("updatesUserId", current_updates_user_id)

        # Steps of priority

        # Discord override
        if self.handler_input.is_discord is True:
            if not len(self.request_handlers_chain) > 0:
                raise Exception(f"No request handlers have been found !!!!!")
            else:
                handler_to_use = list(self.request_handlers_chain.values())[0]

        # First, if the request is an interactive option made by the user
        if self.handler_input.need_to_be_handled_by_callback():
            infos_callback_function_to_use = self.handler_input.interactivity_callback_functions.get(
                self.handler_input.selected_option_identifier
            ).to_safedict(default=None)

            if infos_callback_function_to_use is not None:
                from inoft_vocal_framework.skill_builder import get_function_or_class_from_file_and_path
                handler_to_use = get_function_or_class_from_file_and_path(
                    file_filepath=infos_callback_function_to_use.get("file_filepath_containing_callback").to_str(),
                    path_qualname=infos_callback_function_to_use.get("callback_function_path").to_str())

                if handler_to_use is not None:
                    handler_is_an_alone_callback_function = True

        # Second, Alexa Audio Player
        if self.handler_input.is_alexa:
            if (
                    self.handler_input.alexaHandlerInput.context.audioPlayer is not None and
                    self.handler_input.alexaHandlerInput.context.audioPlayer.token is not None
            ):
                last_used_audioplayer_handlers_group_infos = self.handler_input.alexaHandlerInput.get_last_used_audioplayer_handlers_group()
                from inoft_vocal_framework.skill_builder import get_function_or_class_from_file_and_path
                audioplayer_handlers_group_class_type = get_function_or_class_from_file_and_path(
                    file_filepath=last_used_audioplayer_handlers_group_infos.get("fileFilepathContainingClass").to_str(),
                    path_qualname=last_used_audioplayer_handlers_group_infos.get("classPath").to_str())

                if audioplayer_handlers_group_class_type is not None:
                    raise_if_value_not_in_list(value=InoftHandlersGroup, list_object=list(audioplayer_handlers_group_class_type.__bases__),
                                               variable_name="audioplayer_handlers_group_class_type")

                    class_kwargs = last_used_audioplayer_handlers_group_infos.get("classKwargs").to_dict()
                    class_kwargs["parent_handler"] = self
                    handler_to_use = audioplayer_handlers_group_class_type(**class_kwargs)

                    # When using an audioplayer handlers group, we will call its handle function (it will try every one of its
                    # handler, until he found one that return an output). If the output is None (no function out of every function
                    # of the audioplayer handlers group has returned something), then we will set back the handler_to_use to None,
                    # so that the others more traditional handlers can have a chance to be use (if we did not do that, and that
                    # no event was returned, the response would be the default fallback right away).
                    # The reason we do all of that, is that if the AudioPlayer object is present, but not in a state that is
                    # supported by the app trough a can_handle function (like if it is stopped, and no can_handle function of
                    # any class is triggered by the current state of the AudioPlayer), then we will not be able to give an
                    # interactive experience with the AudioPlayer, which translate into our output_event being None.
                    output_event = handler_to_use.handle()
                    if output_event is not None:
                        handler_is_an_audioplayer_handlers_group = True
                    else:
                        handler_to_use = None

        # Third, if the invocation is a new session, and a session can be resumed, we resume the last intent of the previous session
        if self.handler_input.is_invocation_new_session is True and self.handler_input.session_been_resumed is True:
            last_intent_handler_class_key_name: Optional[str] = self.handler_input.user_data.get_field(field_path='lastIntentHandler')
            if last_intent_handler_class_key_name in self.request_handlers_chain.keys():
                handler_to_use = self.request_handlers_chain[last_intent_handler_class_key_name]
            elif last_intent_handler_class_key_name in self.state_handlers_chain.keys():
                handler_to_use = self.state_handlers_chain[last_intent_handler_class_key_name]

        # Fourth, loading of the then_state in the session
        if handler_to_use is None:
            last_then_state_class_name = self.handler_input.remember_session_then_state()
            if last_then_state_class_name is not None:
                if last_then_state_class_name in self.state_handlers_chain.keys():
                    handler_to_use = self.state_handlers_chain[last_then_state_class_name]
                    handler_is_a_then_state_handler = True
                    self.handler_input.forget_session_then_state()
                else:
                    logging.warning(f"A thenState class name ({last_then_state_class_name}) was not None and has"
                                    f" not been found in the available classes : {self.state_handlers_chain}")

        # Fifth, classical requests handlers
        if handler_to_use is None:
            for request_handler in self.request_handlers_chain.values():
                if request_handler.can_handle() is True:
                    handler_to_use = request_handler
                    handler_is_a_request_handler = True
                    break
                else:
                    logging.debug(f"Not handled by : {request_handler.__class__}")

        if handler_to_use is not None:
            if handler_is_an_alone_callback_function is True:
                output_event = handler_to_use(self.handler_input, self.handler_input.selected_option_identifier)
                if output_event is not None:
                    logging.debug(f"Successfully resumed by {handler_to_use} which returned {output_event}")
                else:
                    logging.info(f"A callback function has been found {handler_to_use}. But nothing was returned,"
                                 f" did you called the return self.to_platform_dict() function ?")

            if output_event is None and self.handler_input.session_been_resumed is True:
                logging.debug(f"Handled and resumed by : {handler_to_use.__class__}")
                output_event = handler_to_use.handle_resume()

            if output_event is None:
                logging.debug(f"Handled classically by : {handler_to_use.__class__}")
                output_event = handler_to_use.handle()
                if handler_is_a_then_state_handler is True and output_event is None:
                    # If the handle function of the a then_state handler do not return anything, we call its fallback
                    # function, and we set back the then_state to the session attributes (we do so before calling
                    # the fallback, in case the fallback function changed the then_state)
                    self.handler_input.memorize_session_then_state(state_handler_class_type_or_name=last_then_state_class_name)
                    output_event = handler_to_use.fallback()

        if output_event is not None:
            if handler_is_an_alone_callback_function is False and handler_is_an_audioplayer_handlers_group is False:
                # If the response is handled by a function, we do not save it as the last intent (we cannot actually,
                # and it would not make sense anyway). So we will keep the previous last intent as the new last intent.
                # We do the same thing it is handler by an audioplayer handlers group (since it is used to handle interactions too)
                self.handler_input.memorize_session_last_intent_handler(handler_class_type_instance_name=handler_to_use)
        else:
            logging.debug(f"Handler by default fallback : {self.default_fallback_handler}")
            output_event = self.default_fallback_handler.handle()

        for callback in self.on_interaction_end:
            callback()

        if self.handler_input.is_discord is not True:
            print(f"output_event = {output_event}")
            wrapped_output_event = LambdaResponseWrapper(response_dict=output_event).get_wrapped(handler_input=self.handler_input)
            return wrapped_output_event
        else:
            return None

    def check_everything_implemented(self):
        if self.default_fallback_handler is None:
            raise Exception(f"A skill must have a {InoftDefaultFallback} handler set with the {self.set_default_fallback_handler} function.")

    @staticmethod
    def _get_alexa_application_id_from_event(event: dict) -> Optional[str]:
        context: Optional[dict] = event.get('context', None)
        if context is not None:
            system: Optional[dict] = context.get('System', None)
            if system is not None:
                application: Optional[dict] = system.get('application', None)
                if application is not None:
                    return application.get('applicationId', None)
        return None

    def handle_any_platform(self, event: dict, context: dict):
        # from inoft_vocal_framework.platforms_handlers.discord.handler_input import DiscordHandlerInput

        print(f"Crude event = {event if not isinstance(event, dict) else json_dumps(event)}\nCrude context = {context}")
        self.check_everything_implemented()

        # The 'rawPath' is for ApiGatewayV2, use the key 'resource' (without the comma) if using ApiGatewayV1
        event_raw_path: Optional[str] = event.get('rawPath', None)

        if event_raw_path == '/googleAssistantDialogflowV1':
            # A google-assistant or dialogflow request always pass trough an API gateway
            self.handler_input.set_platform_to_dialogflow()
            event_body: Optional[dict or str] = event.get('body', None)
            if event_body is None:
                raise Exception("Event body not found")
            event: dict = event_body if isinstance(event_body, dict) else json.loads(event_body)
            print(f"Event body for Google Assistant = {json_dumps(event)}")

        elif event_raw_path == "/samsungBixbyV1":
            # A samsung bixby request always pass trough an API gateway
            self.handler_input.set_platform_to_bixby()
            event_body: Optional[dict] = event.get('body', None)
            if event_body is None:
                raise Exception("Event body not found")

            from urllib import parse
            event_raw_query_string: Optional[str] = event.get('rawQueryString', None)
            parameters: dict = dict(parse.parse_qsl(event_raw_query_string)) if event_raw_query_string is not None else {}

            event = {'context': event_body.get('$vivContext'), 'parameters': parameters}
            print(f"Event body for Samsung Bixby = {json_dumps(event)}")

        elif "amzn1." in (self._get_alexa_application_id_from_event(event=event) or ""):
            # Alexa always go last, since it do not pass trough an api resource, its a less robust identification than the other platforms.
            self.handler_input.set_platform_to_alexa()
            print(f"Event body do not need processing for Alexa : {event}")

        elif False:  # Discord client is currently deprecated    DiscordHandlerInput.SHOULD_BE_USED is True:
            self.handler_input.set_platform_to_discord()
            print(f"Event body do not need processing for Discord : {event}")

        else:
            from inoft_vocal_framework.messages import ERROR_PLATFORM_NOT_SUPPORTED
            raise Exception(ERROR_PLATFORM_NOT_SUPPORTED)

        self.handler_input.load_event(event=event)

        return self.process_request()

    @property
    def request_handlers_chain(self) -> dict:
        return self._request_handlers_chain

    @property
    def state_handlers_chain(self) -> dict:
        return self._state_handlers_chain

    @property
    def default_fallback_handler(self):
        return self._default_fallback_handler

    @default_fallback_handler.setter
    def default_fallback_handler(self, default_fallback_handler) -> None:
        self._default_fallback_handler = default_fallback_handler

    @property
    def handler_input(self) -> HandlerInput:
        return self._handler_input

    @property
    def default_session_data_timeout(self):
        return self._handler_input.default_session_data_timeout

    @default_session_data_timeout.setter
    def default_session_data_timeout(self, default_session_data_timeout: int) -> None:
        if not isinstance(default_session_data_timeout, int):
            raise Exception(f"default_session_data_timeout was type {type(default_session_data_timeout)} which is not valid value for his parameter.")
        self.handler_input._default_session_data_timeout = default_session_data_timeout
