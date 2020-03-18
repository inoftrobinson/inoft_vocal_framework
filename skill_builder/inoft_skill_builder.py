from abc import abstractmethod
from json import dumps as json_dumps
from inoft_vocal_framework.platforms_handlers.endpoints_providers.providers import LambdaResponseWrapper
from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput, HandlerInputWrapper
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.skill_builder.skill_settings import Settings


class InoftRequestHandler(HandlerInputWrapper):  # (HandlerInput):
    @abstractmethod
    def can_handle(self) -> bool:
        """ Returns true if Request Handler can handle the Request inside Handler Input.
        :return: Boolean value that tells the dispatcher if the current request can be handled by this handler.
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    def handle(self):
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def handle_resume(self):
        print(f"Resuming an user session, but no logic has been found in the handle_resume function, defaulting to the handle function")

class InoftStateHandler(HandlerInputWrapper):  # (HandlerInput):
    @abstractmethod
    def handle(self):
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def fallback(self):
        """ Handler if no response has been gotten from the handle method.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        raise NotImplementedError

    @abstractmethod
    def handle_resume(self):
        print(f"Resuming an user session, but no logic has been found in the handle_resume function, defaulting to the handle function")

class InoftDefaultFallback(HandlerInputWrapper):
    @abstractmethod
    def handle(self):
        raise NotImplementedError

class InoftSkill:
    def __init__(self, settings_yaml_filepath=None, settings_json_filepath=None):

        self.settings = Settings()
        if settings_yaml_filepath is not None and settings_json_filepath is not None:
            raise Exception(f"You cannot specify multiple settings files. Please specify only one")
        elif settings_yaml_filepath is None and settings_json_filepath is None:
            raise Exception(f"Please specify a yaml or json settings file with the settings_yaml_filepath arg or settings_json_filepath")
        elif settings_yaml_filepath is not None:
            self.settings.load_yaml(settings_file=settings_yaml_filepath)
        elif settings_json_filepath is not None:
            self.settings.load_json(settings_file=settings_json_filepath)

        self._request_handlers_chain = dict()
        self._state_handlers_chain = dict()
        self._default_fallback_handler = None
        self._handler_input = HandlerInput()

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
        handler_to_use = None
        handler_is_an_alone_callback_function = False
        handler_is_a_then_state_handler = False
        handler_is_a_request_handler = False

        # Steps of priority

        # First, if the request is an interactive option made by the user
        if self.handler_input.is_option_select_request:
            # todo: rename is_option_select_request to need_to_be_handled_by_callback
            infos_callback_function_to_use = self.handler_input.interactivity_callback_functions.get(
                self.handler_input.selected_option_identifier).to_safedict(default=None)

            if infos_callback_function_to_use is not None:
                from inoft_vocal_framework.skill_builder.utils import get_function_from_file_and_path
                handler_to_use = get_function_from_file_and_path(
                    file_filepath=infos_callback_function_to_use.get("file_filepath_containing_callback").to_str(),
                    function_path_qualname=infos_callback_function_to_use.get("callback_function_path").to_str())

                if handler_to_use is not None:
                    handler_is_an_alone_callback_function = True

        # Second, if the invocation is a new session, and a session can be resumed, we resume the last intent of the previous session
        if self.handler_input.is_invocation_new_session is True and self.handler_input.session_been_resumed is True:
            last_intent_handler_class_key_name = self.handler_input.session_remember("lastIntentHandler")
            if last_intent_handler_class_key_name in self.request_handlers_chain.keys():
                handler_to_use = self.request_handlers_chain[last_intent_handler_class_key_name]
            elif last_intent_handler_class_key_name in self.state_handlers_chain.keys():
                handler_to_use = self.state_handlers_chain[last_intent_handler_class_key_name]

        # Third, loading of the then_state in the session
        if handler_to_use is None:
            last_then_state_class_name = self.handler_input.remember_session_then_state()
            if last_then_state_class_name is not None:
                if last_then_state_class_name in self.state_handlers_chain.keys():
                    handler_to_use = self.state_handlers_chain[last_then_state_class_name]
                    handler_is_a_then_state_handler = True
                    self.handler_input.forget_session_then_state()
                else:
                    print(f"Warning ! A thenState class name ({last_then_state_class_name}) was not None"
                          f" and has not been found in the available classes : {self.state_handlers_chain}")

        # Fourth, classical requests handlers
        if handler_to_use is None:
            for request_handler in self.request_handlers_chain.values():
                if request_handler.can_handle() is True:
                    handler_to_use = request_handler
                    handler_is_a_request_handler = True
                    break
                else:
                    print(f"Not handled by : {request_handler.__class__}")

        output_event = None
        if handler_to_use is not None:
            if handler_is_an_alone_callback_function is True:
                output_event = handler_to_use(self.handler_input, self.handler_input.selected_option_identifier)
                if output_event is not None:
                    print(f"Successfully resumed by {handler_to_use} which returned {output_event}")
                else:
                    print(f"A callback function has been found {handler_to_use}. But nothing was returned,"
                          f"did you called the return self.to_platform_dict() function ?")

            if output_event is None and self.handler_input.session_been_resumed is True:
                print(f"Handled and resumed by : {handler_to_use.__class__}")
                output_event = handler_to_use.handle_resume()

            if output_event is None:
                print(f"Handled classically by : {handler_to_use.__class__}")
                output_event = handler_to_use.handle()
                if handler_is_a_then_state_handler is True and output_event is None:
                    # If the handle function of the a then_state handler do not return anything, we call its fallback
                    # function, and we set back the then_state to the session attributes (we do so before calling
                    # the fallback, in case the fallback function changed the then_state)
                    self.handler_input.memorize_session_then_state(state_handler_class_type_or_name=last_then_state_class_name)
                    output_event = handler_to_use.fallback()

        if output_event is not None:
            if handler_is_an_alone_callback_function is False:
                # If the response is handled by a function, we do not save it as the last intent (we cannot actually,
                # and it would not make sense anyway). So we will keep the previous last intent as the new last intent.
                self.handler_input.memorize_session_last_intent_handler(handler_class_type_instance_name=handler_to_use)
        else:
            print(f"Handler by default fallback : {self.default_fallback_handler}")
            output_event = self.default_fallback_handler.handle()

        self.handler_input.save_attributes_if_need_to()

        print(f"output_event = {output_event}")
        wrapped_output_event = LambdaResponseWrapper(response_dict=output_event).get_wrapped(handler_input=self.handler_input)
        return wrapped_output_event

    def check_everything_implemented(self):
        if self.default_fallback_handler is None:
            raise Exception(f"A skill must have a {InoftDefaultFallback} handler set with the {self.set_default_fallback_handler} function.")

    def handle_any_platform(self, event: dict, context: dict):
        print(f"Event = {json_dumps(event)}\nContext = {context}")
        self.check_everything_implemented()
        event_safedict = SafeDict(classic_dict=event)

        if event_safedict.get("resource").to_str() == "/google-assistant-v1":
            # A google-assistant or dialogflow request always pass trough an API gateway
            self.handler_input.is_dialogflow_v1 = True
            event = NestedObjectToDict.get_dict_from_json(event_safedict.get("body").to_str())

        elif event_safedict.get("resource").to_str() == "/samsung-bixby-v1":
            # A samsung bixby request always pass trough an API gateway
            self.handler_input.is_bixby_v1 = True
            event = NestedObjectToDict.get_dict_from_json(event_safedict.get("body").to_str())

        elif "amzn1." in event_safedict.get("context").get("System").get("application").get("applicationId").to_str():
            # Alexa always go last, since it do not pass trough an api resource, its a less robust identification than the other platforms.
            self.handler_input.is_alexa_v1 = True
        else:
            from inoft_vocal_framework.messages import ERROR_PLATFORM_NOT_SUPPORTED
            raise Exception(ERROR_PLATFORM_NOT_SUPPORTED)

        self.handler_input.load_event_and_context(event=event, context=context)
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
