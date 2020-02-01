from inoft_vocal_framework.safe_dict import SafeDict


def process_event(event_input: SafeDict) -> dict:
    try:
        event = dict()
        event["isBase64Encoded"] = False
        event["statusCode"] = 200
        event["headers"] = dict()

        event_body = event_input.get("body").to_dict()
        event_body["version"] = "1.0"

        event["body"] = str(event_body)
        return event
    except Exception as error:
        print(f"Error happened while processing the google assistant request : {error}")
        return dict()
