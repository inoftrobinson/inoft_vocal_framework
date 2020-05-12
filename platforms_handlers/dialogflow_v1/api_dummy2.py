import io
import json

import requests
from google.oauth2 import service_account
import google.auth.transport.requests

PATH_TO_SERVICE_ACCOUNT = "C:/Users/LABOURDETTE/Downloads/jeu-seconde-guerre-mondiale-84a61cf2b3ca.json"

REQUIRED_SCOPE = "https://www.googleapis.com/auth/actions.fulfillment.conversation"

# Get access token
with io.open(PATH_TO_SERVICE_ACCOUNT, "r", encoding="utf-8") as json_fi:
    credentials_info = json.load(json_fi)

credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=[REQUIRED_SCOPE])
request = google.auth.transport.requests.Request()
credentials.refresh(request)

headers = {
    "Authorization": "Bearer " + credentials.token
}

payload = {
    "customPushMessage": {
        "userNotification": {
            "title": "Notification title",
            "text": "Simple Text"
        },
        "target": {
            "userId": "<USER_ID>",
            "intent": "actions.intent.MAIN",
            "locale": "fr-FR"
        }
    }
}

r = requests.request("POST", "https://actions.googleapis.com/v2/conversations:send", data=json.dumps(payload), headers=headers)
print(str(r.status_code) + ": " + r.text)
