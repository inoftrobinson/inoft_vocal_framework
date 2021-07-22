import unittest
from typing import Optional, Any

from inoft_vocal_framework import Settings
from inoft_vocal_framework.platforms_handlers import handler_input


class TestResample(unittest.TestCase):
    def test_basic_messages(self):
        handler = handler_input.HandlerInput(settings_instance=Settings(
            engine_account_id="b1fe5939-032b-462d-92e0-a942cd445096",
            engine_project_id="4ede8b70-46f6-4ae2-b09c-05a549194c8e",
            engine_api_key="a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
        ))

        handler._force_load_alexa()
        handler.say("One")
        handler.say("Two")
        self.assertEqual(handler.alexa.response.outputSpeech.text, "One\nTwo")

        update_success: bool = handler.user_data.update_field(
            field_path='lastIntentHandler', value_to_set="dummy"
        )
        operations_commit_success: bool = handler.user_data.commit_operations()

        retrieved_field_data: Optional[Any] = handler.user_data.get_field(
            field_path='lastIntentHandler'
        )
        print(retrieved_field_data)

        """handler._force_load_dialogflow()
        handler.say("One")
        handler.say("Two")
        self.assertEqual(handler.google.response.payload.google.richResponse.items[0].textToSpeech, "One\nTwo")"""


if __name__ == '__main__':
    unittest.main()
