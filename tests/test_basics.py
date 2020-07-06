from inoft_vocal_engine.platforms_handlers import handler_input

def basic_messages():
    handler = handler_input.HandlerInput()

    handler._force_load_alexa()
    handler.say("One")
    handler.say("Two")
    assert handler.alexa.response.outputSpeech.text == "One\nTwo"

    handler._force_load_dialogflow()
    handler.say("One")
    handler.say("Two")
    assert handler.google.response.payload.google.richResponse.items[0].textToSpeech == "One\nTwo"

basic_messages()
