import unittest

from inoft_vocal_framework import Settings
from inoft_vocal_framework.platforms_handlers import handler_input


class TestResample(unittest.TestCase):
    def basic_messages(self):
        handler = handler_input.HandlerInput(settings_instance=Settings())

        handler._force_load_alexa()
        handler.say("One")
        handler.say("Two")
        self.assertEqual(handler.alexa.response.outputSpeech.text, "One\nTwo")

        handler._force_load_dialogflow()
        handler.say("One")
        handler.say("Two")
        self.assertEqual(handler.google.response.payload.google.richResponse.items[0].textToSpeech, "One\nTwo")


if __name__ == '__main__':
    unittest.main()
