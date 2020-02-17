from inoft_vocal_framework.platforms_handlers.handler_input import HandlerInput


class Test(object):
    def __new__(cls, handler_input: HandlerInput):
        return object.__new__(cls)

aaa = HandlerInput()
class Touste(Test(aaa)):
    pass

Touste()

Test(handler_input=aaa)
