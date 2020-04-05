import os

import inflect as inflect

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.general import load_json
from jinja2 import Template, FileSystemLoader, Environment


class Templates:
    def __init__(self):
        self._state_handler = None

    @property
    def state_handler(self) -> str:
        if self._state_handler is None:
            self._state_handler = """"""
        return self._state_handler

class StateHandler:
    def __init__(self, class_name: str, code: str):
        self.class_name = class_name
        self.code = code

    class Path:
        CONDITION_TYPE_INTENT_NAME = "intent_name"

        def __init__(self, condition: str, target_node: str):
            self.condition_type = None
            self.condition_intent_name = None
            self.target_node = target_node
            self.process_condition(condition=condition)

        def process_condition(self, condition: str):
            if "event.nlu.intent.name ===" in condition:
                self.condition_type = self.CONDITION_TYPE_INTENT_NAME
                self.condition_intent_name = turn_numbers_to_word_in_text(condition.replace("event.nlu.intent.name ===", "")
                                                                          .replace(" ", "").replace("'", "").replace('"', ''))
            else:
                self.condition_type = None
                self.condition_intent_name = "Generic"
                # raise Exception("Condition type not supported.")

    @staticmethod
    def process_paths(paths: list) -> list:
        for i, path in enumerate(paths):
            path = SafeDict(path)
            paths[i] = StateHandler.Path(condition=path.get("condition").to_str(default=None),
                                         target_node=path.get("node").to_str(default=None))
        return paths

def turn_numbers_to_word_in_text(text: str) -> str:
    new_text = ""
    current_digit_sequence = ""
    for i, char in enumerate(text):
        if str(char).isdigit():
            current_digit_sequence += char
        elif current_digit_sequence != "":
            new_text += inflect.engine().number_to_words(current_digit_sequence)
            current_digit_sequence = ""
        else:
            new_text += char

    text_elements = new_text.split("-")
    for text_element in text_elements:
        new_text = text_element[0].capitalize() + text_element[1:]

    return new_text


def flow_to_handlers(flow_filepath: str, builtin_text_filepath: str):
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)
    state_template = env.get_template("state_handler.tem")
    skill_app_template = env.get_template("skill_app.tem")

    flow_dict = load_json(filepath=flow_filepath)
    if "nodes" not in flow_dict.keys():
        raise Exception(f"The nodes key has not been found in the dict of the flow_file : {flow_dict}")
    else:
        state_handlers_list = list()

        nodes_list = flow_dict["nodes"]
        for node in nodes_list:
            node = SafeDict(node)
            class_name = turn_numbers_to_word_in_text(node.get("name").to_str())
            rendered_node_code = state_template.render(class_name=class_name, paths=StateHandler.process_paths(paths=node.get("next").to_list()))
            state_handlers_list.append(StateHandler(class_name=f"{class_name}StateHandler", code=rendered_node_code))

        skill_app_rendered_code = skill_app_template.render(request_handlers=[],
                                                            state_handlers=state_handlers_list)
        write_to_file(text=skill_app_rendered_code, filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.py"))

def write_to_file(text: str, filepath: str):
    with open(filepath, "w+") as file:
        file.write(text)


flow_to_handlers("F:\Inoft\skill_histoire_decryptage_1\inoft_vocal_framework\project_bt_generator\main.flow.json",
                 "F:\Inoft\skill_histoire_decryptage_1\inoft_vocal_framework\project_bt_generator/builtin_text.json")

"""
 "id": "0800afbc29",
  "name": "node-deb1",
  "next": [
    {
      "condition": "event.nlu.intent.name === 'yes'",
      "node": "node-fa51"
    },
    {
      "condition": "event.nlu.intent.name === 'no'",
      "node": "node-2d79"
    }
  ],
  "onEnter": [
    "say #!builtin_text--FWw96"
  ],
  "onReceive": null,
  "type": "standard"
"""
