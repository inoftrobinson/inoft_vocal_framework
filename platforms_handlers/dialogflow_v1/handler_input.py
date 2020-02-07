from inoft_vocal_framework.platforms_handlers.dialogflow_v1.request import Request
from inoft_vocal_framework.platforms_handlers.dialogflow_v1.response import Response, SimpleResponse


class DialogFlowHandlerInput:
    request = Request()
    response = Response()

    @staticmethod
    def get_user_persistent_data():
        unprocessed_user_stored_data = DialogFlowHandlerInput.request.originalDetectIntentRequest.payload.user.userStorage
        if isinstance(unprocessed_user_stored_data, str) and unprocessed_user_stored_data.replace(" ", "") != "":
            from unicodedata import normalize as unicode_normalize
            from ast import literal_eval
            try:
                user_stored_data = literal_eval(unicode_normalize("NFD", unprocessed_user_stored_data))
                if isinstance(user_stored_data, dict):
                    return user_stored_data
                else:
                    print(f"Non-crashing error, the user_stored_data has been retrieved and converted from a string, but was but {type(user_stored_data)} and need to be a dict")
                    return None
            except Exception as e:
                print(f"Error while processing the user_persistent_data. Non-crashing but returning None : {e}")
        return None

    @staticmethod
    def get_user_id():
        persistent_data = DialogFlowHandlerInput.get_user_persistent_data()
        if not isinstance(persistent_data, dict) or "userId" not in persistent_data.keys():
            return None
        else:
            return persistent_data["userId"]

    @staticmethod
    def say(text_or_ssml: str) -> None:
        # todo: allow to have 2 differents response in the same one, not just one
        output_response = SimpleResponse()
        output_response.textToSpeech = text_or_ssml
        DialogFlowHandlerInput.response.payload.google.richResponse.add_response_item(output_response)


"""
{
  "originalDetectIntentRequest": {
    "source": "google",
    "version": "2",
    "payload": {
      "user": {
        "locale": "fr-CA",
        "lastSeen": "2020-02-05T14:05:59Z",
        "userStorage": "{'akey': 1000}",
        "userVerificationStatus": "VERIFIED"
      },
      "conversation": {
        "conversationId": "ABwppHGHHaD_iGo2Au44c9amNN82OktseI45PrdSpCsZohIPWcOIowLMAumG3dsroSjcZn3D-mnVMjrggtnA35g",
        "type": "NEW"
      },
      "inputs": [
        {
          "intent": "actions.intent.MAIN",
          "rawInputs": [
            {
              "inputType": "VOICE",
              "query": "Parler avec Cité des sciences"
            }
          ]
        }
      ],
      "surface": {
        "capabilities": [
          {
            "name": "actions.capability.AUDIO_OUTPUT"
          },
          {
            "name": "actions.capability.ACCOUNT_LINKING"
          },
          {
            "name": "actions.capability.MEDIA_RESPONSE_AUDIO"
          },
          {
            "name": "actions.capability.SCREEN_OUTPUT"
          }
        ]
      },
      "isInSandbox": true,
      "availableSurfaces": [
        {
          "capabilities": [
            {
              "name": "actions.capability.AUDIO_OUTPUT"
            },
            {
              "name": "actions.capability.SCREEN_OUTPUT"
            },
            {
              "name": "actions.capability.WEB_BROWSER"
            }
          ]
        }
      ],
      "requestType": "SIMULATOR"
    }
  },
  "session": "projects/cite-des-sciences/agent/sessions/ABwppHGHHaD_iGo2Au44c9amNN82OktseI45PrdSpCsZohIPWcOIowLMAumG3dsroSjcZn3D-mnVMjrggtnA35g"
}
"""
