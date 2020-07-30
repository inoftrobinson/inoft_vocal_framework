import json
from inoft_vocal_engine.inoft_vocal_framework.platforms_handlers.nested_object_to_dict import NestedObjectToDict

filepath = "/inoft_vocal_engine/platforms_handlers/simulator/request_samples/google/launch.json"
with open(filepath, "r") as file:
    event_str = json.load(file)
    event_body_dict = NestedObjectToDict.get_dict_from_json(stringed_json_dict=event_str["body"])
    print(json.dumps(event_body_dict))

