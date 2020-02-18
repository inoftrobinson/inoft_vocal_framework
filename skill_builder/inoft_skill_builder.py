from abc import abstractmethod
from json import dumps as json_dumps
from inoft_vocal_framework.platforms_handlers.endpoints_providers.providers import LambdaResponseWrapper
from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput, HandlerInputWrapper
from inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict
from inoft_vocal_framework.safe_dict import SafeDict


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

class InoftDefaultFallback(HandlerInputWrapper):
    @abstractmethod
    def handle(self):
        raise NotImplementedError

class InoftSkill:
    def __init__(self, db_table_name: str, db_region_name=None):
        self._request_handlers_chain = list()
        self._state_handlers_chain = dict()
        self._default_fallback_handler = None
        self._handler_input = HandlerInput(db_table_name=db_table_name, db_region_name=db_region_name)

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
                    self.request_handlers_chain.append(request_handler_instance_or_class)
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

                if InoftRequestHandler in handler_bases_parent_classes:
                    default_fallback_handler_instance_or_class.handler_input = self.handler_input
                    # We set a reference to the skill handler_input in each handler so that it can use it with its HandlerInputWrapper
                    self.request_handlers_chain.append(default_fallback_handler_instance_or_class)

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
        handler_is_a_then_state_handler = False
        handler_is_a_request_handler = False

        last_then_state_class_name = self.handler_input.remember_session_then_state()
        if last_then_state_class_name is not None:
            if last_then_state_class_name in self.state_handlers_chain.keys():
                handler_to_use = self.state_handlers_chain[last_then_state_class_name]
                handler_is_a_then_state_handler = True
                self.handler_input.forget_session_then_state()
            else:
                print(f"Warning ! A thenState class name ({last_then_state_class_name}) was not None"
                      f" and has not been found in the available classes : {self.state_handlers_chain}")

        if handler_to_use is None:
            for request_handler in self.request_handlers_chain:
                if request_handler.can_handle() is True:
                    handler_to_use = request_handler
                    handler_is_a_request_handler = True
                    break
                else:
                    print(f"Not handled by : {request_handler.__class__}")

        output_event = None
        if handler_to_use is not None:
            print(f"Handled by : {handler_to_use.__class__}")
            output_event = handler_to_use.handle()
            if handler_is_a_then_state_handler is True:
                if output_event is None:
                    # If the handle function of the a then_state handler do not return anything, we call its fallback
                    # function, and we set back the then_state to the session attributes (we do so before calling
                    # the fallback, in case the fallback function changed the then_state)
                    self.handler_input.memorize_session_then_state(state_handler_class_type_or_name=last_then_state_class_name)
                    output_event = handler_to_use.fallback()

        if output_event is None:
            print(f"Handler by default fallback : {self.default_fallback_handler}")
            output_event = self.default_fallback_handler.handle()

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
    def request_handlers_chain(self):
        return self._request_handlers_chain

    @property
    def state_handlers_chain(self):
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
