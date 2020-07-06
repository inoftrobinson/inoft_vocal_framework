from json import dumps as json_dumps
from inoft_vocal_engine.platforms_handlers.handler_input import HandlerInput


class LambdaResponseWrapper:
    def __init__(self, response_dict: dict):
        if not isinstance(response_dict, dict):
            raise Exception(f"The response_dict must be of type dict and is of type : {type(response_dict)}")

        self._response_dict = response_dict

    def get_wrapped(self, handler_input: HandlerInput) -> dict:
        if handler_input.is_alexa is True:
            return self._response_dict

        elif (handler_input.is_dialogflow is True
        or handler_input.is_bixby is True):
            return {
                "isBase64Encoded": False,
                "statusCode": 200,
                "headers": dict(),
                "body": json_dumps(self._response_dict)
            }

        else:
            raise Exception(f"Platform is not supported.")
