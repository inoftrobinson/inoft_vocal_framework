import json

filepath = "/inoft_vocal_framework/platforms_handlers/simulator/request_samples/google/launch.json"
with open(filepath, "r") as file:
    event: dict = json.load(file)
    event_dict = json.loads(event['body'])
    print(json.dumps(event_dict))

