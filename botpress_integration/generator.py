import os

import inflect as inflect

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.general import load_json
from inoft_vocal_framework.project_bt_generator.templates.templates_access import TemplatesAccess
from jinja2 import Template, FileSystemLoader, Environment

def process_node_name(text: str) -> str:
    new_text = ""
    current_digit_sequence = ""
    for i, char in enumerate(text):
        # We add a - when adding numbers, so that they will be considered as separate
        # element in the class name, and that their first letter will be capitalized.
        if str(char).isdigit():
            current_digit_sequence += char
            if i+1 == len(text):
                new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
                current_digit_sequence = ""
        elif current_digit_sequence != "":
            new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
            current_digit_sequence = ""
        else:
            new_text += char

    formatted_output_text = ""
    text_elements = new_text.split("-")
    for text_element in text_elements:
        formatted_output_text += ((text_element[0].capitalize() if len(text_element) > 0 else "") +
                                  (text_element[1:] if len(text_element) > 1 else ""))

    return formatted_output_text

class Core:
    def __init__(self, main_flow_filepath: str = None, builtin_text_filepath: str = None):
        self.main_flow_filepath = main_flow_filepath
        self.builtin_text_filepath = builtin_text_filepath
        self.has_request_handlers = False
        self.has_state_handlers = False
        self.messages = None

        self.node_values_dict = dict()
        self.node_classes_dict = dict()

    def process(self):
        self.messages = Messages(messages_items=load_json(self.builtin_text_filepath))
        self.write_to_file(text=self.messages.render(), filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "messages.py"))

        flow_dict = load_json(filepath=self.main_flow_filepath)
        if "nodes" not in flow_dict.keys():
            raise Exception(f"The nodes key has not been found in the dict of the flow_file : {flow_dict}")
        else:
            name_start_node = flow_dict["startNode"]
            nodes_list = flow_dict["nodes"]
            # Initialization of the classes
            for node in nodes_list:
                node_name = node["name"] or ""
                self.node_values_dict[node_name] = node

                if node_name == name_start_node:
                    self.node_classes_dict[node_name] = LaunchRequestHandler(node_dict=node)
                    self.has_request_handlers = True
                else:
                    self.node_classes_dict[node_name] = StateHandler(node_name=node_name)
                    self.has_state_handlers = True

            # Processing of the classes and their interactions with each others
            for node_class in self.node_classes_dict.values():
                node_class.process(parent_core=self)

            output_handlers_list = list()
            for class_from_node in self.node_classes_dict.values():
                for handler_class in class_from_node.render(parent_core=self):
                    output_handlers_list.append(handler_class)

            skill_app_rendered_code = TemplatesAccess().skill_app_template.render(handlers_list=output_handlers_list,
                                                                                  has_request_handlers=self.has_request_handlers,
                                                                                  has_state_handlers=self.has_state_handlers)

            self.write_to_file(text=skill_app_rendered_code, filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.py"))

    def process_on_enter(self, actions_list: list) -> str:
        message_dict = None

        for action in actions_list:
            if isinstance(action, str) and len(action) >= 3:
                if action[0:3] == "say":
                    if "#!builtin_text" in action:
                        message_name = action.replace("say", "").replace("#!", "").replace(" ", "")
                        if message_name in self.messages.output_messages_dict.keys():
                            message_element = f"{self.messages.output_messages_dict[message_name].variable_name}.pick()"
                            is_callable = True
                        else:
                            message_element = message_name
                            is_callable = False

                        message_dict = {"name": message_name, "element": message_element, "is_callable": is_callable}

        output_code = TemplatesAccess().handler_logic_template.render(message=message_dict)
        return output_code

    @staticmethod
    def write_to_file(text: str, filepath: str):
        with open(filepath, "w+") as file:
            file.write(text)


class StateHandler:
    CLASS_TYPE = "StateHandler"

    def __init__(self, node_name: str):
        self.node_name = node_name
        self.class_name = process_node_name(self.node_name)
        self.code = None
        self.next_paths = list()

    class Path:
        CONDITION_TYPE_INTENT_NAME = "intent_name"

        def __init__(self, condition: str, target_node_name: str):
            self.condition_str = condition
            self.condition_type = None
            self.condition_intent_name = None
            self.target_node_name = target_node_name
            self.target_node_class = f"{process_node_name(target_node_name or '')}StateHandler"
            self.code = None

        def process(self, parent_core: Core):
            if self.condition_str is not None and "event.nlu.intent.name ===" in self.condition_str:
                self.condition_type = self.CONDITION_TYPE_INTENT_NAME
                self.condition_intent_name = process_node_name(self.condition_str.replace("event.nlu.intent.name ===", "")
                                                               .replace(" ", "").replace("'", "").replace('"', ''))
                self.code = parent_core.process_on_enter(parent_core.node_values_dict[self.target_node_name]["onEnter"]).lstrip("\n")
                if self.code == "":
                    self.code = None
            else:
                self.condition_type = None
                self.condition_intent_name = "Generic"
                # raise Exception("Condition type not supported.")

    @staticmethod
    def process_paths(parent_core: Core, paths: list) -> list:
        processed_paths = list()

        for i, path in enumerate(paths):
            path = SafeDict(path)
            path_condition = path.get("condition").to_str(default=None)
            path_target_node_name = path.get("node").to_str(default=None)

            if path_condition is not None and path_target_node_name is not None:
                current_path_instance = StateHandler.Path(condition=path_condition, target_node_name=path_target_node_name)
                current_path_instance.process(parent_core=parent_core)
                processed_paths.append(current_path_instance)

        return processed_paths

    def get_code(self, parent_core: Core) -> str:
        if self.code is None:
            self.render(parent_core=parent_core)
        return self.code

    def process(self, parent_core: Core):
        self.next_paths = self.process_paths(parent_core=parent_core, paths=self.next_paths if len(self.next_paths) > 0 else parent_core.node_values_dict[self.node_name]["next"])

    def render(self, parent_core: Core):
        self.code = TemplatesAccess().state_handler_template.render(class_name=self.class_name, paths=self.next_paths)
        return [self]

class LaunchRequestHandler:
    CLASS_TYPE = "RequestHandler"

    def __init__(self, node_dict: dict):
        self.node_safedict = SafeDict(node_dict)
        self.node_name = self.node_safedict.get("name").to_str()
        self.class_name = process_node_name(self.node_name)
        self.code = None
        self.state_handler_class = None

    def process(self, parent_core: Core):
        next_paths = self.node_safedict.get("next").to_list()
        if len(next_paths) > 0:
            self.state_handler_class = StateHandler(node_name=self.node_name)
            for path in next_paths:
                self.state_handler_class.next_paths.append(path)  # all_nodes_classes_dict[next_paths[0]["name"]]

    def render(self, parent_core: Core):  # dict, parent_all_nodes_classes_dict: dict):
        created_classes = list()

        next_state_handler_class = None
        if self.state_handler_class is not None:
            state_handler = StateHandler(node_name=self.node_name)
            state_handler.process(parent_core=parent_core)
            state_handler.render(parent_core=parent_core)
            created_classes.append(state_handler)
            next_state_handler_class = f"{self.class_name}StateHandler"

        self.code = TemplatesAccess().launch_request_handler_template.render(class_name=self.class_name, next_state_handler_class=next_state_handler_class,
                                                                             handler_logic_code=parent_core.process_on_enter(self.node_safedict.get("onEnter").to_list()))

        created_classes.insert(0, self)
        # We always want for the request handler to be the first element in the classes.
        return created_classes

class Messages:
    def __init__(self, messages_items: dict):
        self.input_messages_items = messages_items
        self.output_messages_dict = dict()
        self.process()

    class MessageItem:
        def __init__(self, id_value: str, speech_items: list):
            self.id = id_value
            self.speechs = speech_items
            self.variable_name = "".join([char.capitalize() for char in self.id.replace("-", "_")])

    def process(self):
        for message_dict in self.input_messages_items:
            message_dict = SafeDict(message_dict)
            speech_items = list()

            main_speech_text = message_dict.get("formData").get("text$en").to_str(default=None)  # todo: make multilang (might require the premium version of botpress)
            if main_speech_text is not None:
                speech_items.append(main_speech_text)
            variations_speechs_texts = message_dict.get("formData").get("variations$en").to_list(default=None)
            if variations_speechs_texts is not None:
                for speech_variation in variations_speechs_texts:
                    speech_items.append(speech_variation)

            message_item = self.MessageItem(id_value=message_dict.get("id").to_str(), speech_items=speech_items)
            self.output_messages_dict[message_item.id] = message_item

    def render(self):
        code_messages_file = TemplatesAccess().messages_template.render(messages=self.output_messages_dict.values())
        return code_messages_file



Core(main_flow_filepath="F:\Inoft\skill_histoire_decryptage_1\inoft_vocal_framework\project_bt_generator\main.flow.json",
     builtin_text_filepath="F:\Inoft\skill_histoire_decryptage_1\inoft_vocal_framework\project_bt_generator/builtin_text.json").process()