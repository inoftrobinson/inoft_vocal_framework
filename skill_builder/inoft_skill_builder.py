from abc import abstractmethod

from inoft_vocal_framework.platforms_handlers.endpoints_providers.providers import LambdaResponseWrapper
from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput

class InoftRequestHandler(HandlerInput):
    @abstractmethod
    def can_handle(self) -> bool:
        """ Returns true if Request Handler can handle the Request inside Handler Input.
        :return: Boolean value that tells the dispatcher if the current request can be handled by this handler.
        :rtype: bool
        """
        # :type handler_input: HandlerInput
        raise NotImplementedError

    @abstractmethod
    def handle(self):
        """Handles the Request inside handler input and provides a Response for dispatcher to return.
        :return: Response for the dispatcher to return or None
        :rtype: Union[Response, None]
        """
        # :type handler_input: HandlerInput
        raise NotImplementedError


class InoftSkill:
    def __init__(self):
        import array
        self._request_handlers_chain = list()

    @property
    def request_handlers_chain(self):
        return self._request_handlers_chain

    def add_request_handler(self, request_handler_instance) -> None:
        if request_handler_instance is not None and isinstance(request_handler_instance, object):
            handler_bases_parent_classes = request_handler_instance.__class__.__bases__

            handler_bases_parent_classes_names = list()
            for handler_base_parent_class in handler_bases_parent_classes:
                handler_bases_parent_classes_names.append(handler_base_parent_class.__name__)

            if InoftRequestHandler.__name__ in handler_bases_parent_classes_names:
                self.request_handlers_chain.append(request_handler_instance)
            return None

        raise Exception(f"The following request handler is not a valid handler or do not have {InoftRequestHandler.__name__} as its MetaClass : {request_handler_instance}")

    def process_request(self):
        for handler in self.request_handlers_chain:
            if handler.can_handle() is True:
                print(f"Handled by : {handler.__class__}")
                output_event = handler.handle()
                wrapped_output_event = LambdaResponseWrapper(response_dict=output_event).get_wrapped()
                return wrapped_output_event
            else:
                print(f"Not handled by : {handler.__class__}")
        return None
