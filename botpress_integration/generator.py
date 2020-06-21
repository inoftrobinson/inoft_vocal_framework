import ast
import os
from typing import Dict, List, Optional

import inflect as inflect

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, \
    raise_if_variable_not_expected_type_and_not_none
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.general import load_json
from inoft_vocal_framework.botpress_integration.templates.templates_access import TemplatesAccess

# todo: fix bug with node where no text is played (it will jump the node itself, and the next node x)  )

def prettify_speech_text(text: str) -> str:
    new_text = str()
    last_char_index_to_have_been_added_new_line = 0
    for i_char, char in enumerate(text):
        if i_char > last_char_index_to_have_been_added_new_line + 115:
            if char == " ":
                new_text += (char + "\n")
                last_char_index_to_have_been_added_new_line = i_char
            else:
                new_text += char
        else:
            new_text += char
    return new_text


def to_class_name(text: str) -> str:
    new_text = ""
    current_digit_sequence = ""
    number_last_char_index = None
    for i, char in enumerate(text):
        # We add a - when adding numbers, so that they will be considered as separate
        # element in the class name, and that their first letter will be capitalized.
        if str(char).isdigit():
            current_digit_sequence += char
            if i+1 == len(text):
                new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
                current_digit_sequence = ""
        else:
            if current_digit_sequence != "":
                new_text += ("-" + inflect.engine().number_to_words(current_digit_sequence))
                current_digit_sequence = ""
                number_last_char_index = i

            if number_last_char_index is not None and number_last_char_index == i:
                char = char.capitalize()
            new_text += char

    formatted_output_text = ""
    half_text_elements = new_text.replace(",", "").split("-")
    final_text_elements = list()
    for text_element in half_text_elements:
        for splitted_element in text_element.split(" "):
            final_text_elements.append(splitted_element)

    for text_element in final_text_elements:
        formatted_output_text += ((text_element[0].capitalize() if len(text_element) > 0 else "") +
                                  (text_element[1:] if len(text_element) > 1 else ""))

    return formatted_output_text

class GeneratorCore:
    def __init__(self, main_flow_filepath: str = None, builtin_text_filepath: str = None):
        self.main_flow_filepath = main_flow_filepath
        self.builtin_text_filepath = builtin_text_filepath
        self.has_conditions_classes = False
        self.has_request_handlers = False
        self.has_state_handlers = False
        self.messages = None

        self.threshold_of_intent_use_to_create_a_condition = 2

        self.counts_used_condition_intent_names = dict()
        self.node_values_dict = dict()
        self.node_classes_dict = dict()

        self.templates = TemplatesAccess()
        self._plugins = None
        self.plugins_folder_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")

        self.say_actions: List[SayAction] = list()
        self.set_variables_actions: List[SetVariableAction] = list()

    @property
    def plugins(self) -> list:
        if self._plugins is None:
            self.plugins_folder_dir = os.path.dirname(os.path.abspath(__file__))

    def process(self):
        self.messages = Messages(messages_items=load_json(self.builtin_text_filepath))
        self.write_to_file(text=self.messages.render(parent_core=self), filepath="F:/Inoft/skill_histoire_decryptage_1/messages.py")
        # os.path.join(os.path.dirname(os.path.abspath(__file__)), "messages.py"))

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

                if isinstance(node_class, StateHandler):
                    for intent_key, count_value in node_class.counts_used_condition_intent_names.items():
                        if intent_key in self.counts_used_condition_intent_names.keys():
                            self.counts_used_condition_intent_names[intent_key] += count_value
                        else:
                            self.counts_used_condition_intent_names[intent_key] = count_value

            output_conditions_classes = list()
            for intent_key, count_value in self.counts_used_condition_intent_names.items():
                if count_value >= self.threshold_of_intent_use_to_create_a_condition:
                    new_intent_name_condition_class = IntentNameCondition(intent_name=intent_key)
                    new_intent_name_condition_class.render(parent_core=self)
                    output_conditions_classes.append(new_intent_name_condition_class)
                    self.has_conditions_classes = True

            output_handlers_list = list()
            for class_from_node in self.node_classes_dict.values():
                for handler_class in class_from_node.render(parent_core=self):
                    output_handlers_list.append(handler_class)

            skill_app_rendered_code = self.templates.skill_app_template.render(conditions_classes_list=output_conditions_classes,
                handlers_list=output_handlers_list, has_condition_classes=self.has_conditions_classes,
                has_request_handlers=self.has_request_handlers, has_state_handlers=self.has_state_handlers)

            self.write_to_file(text=skill_app_rendered_code, filepath="F:/Inoft/skill_histoire_decryptage_1/app_generated.py")

    def process_on_enter(self, actions_list: list) -> list:
        self.say_actions.clear()
        logic_elements = list()

        for action in actions_list:
            if isinstance(action, str):
                if len(action) >= 3:
                    if action[0:3] == "say":
                        if "#!builtin_text" in action:
                            current_say_action = SayAction()
                            current_say_action.message_id_to_say = action.replace("say", "").replace("#!", "").replace(" ", "")

                            if current_say_action.message_id_to_say in self.messages.output_messages_dict.keys():
                                current_say_action.message_item_to_say = self.messages.output_messages_dict[current_say_action.message_id_to_say]
                            else:
                                current_say_action.text_to_say_if_message_item_missing = f"The message with id {current_say_action.message_id_to_say} is missing"

                            self.say_actions.append(current_say_action)

                if "/setVariable" in action:
                    processed_action_list = action.split('{', maxsplit=1)
                    if len(processed_action_list) > 1:
                        processed_action_dict = ast.literal_eval("{" + processed_action_list[1].replace("}", "") + "}")
                        if isinstance(processed_action_dict, dict):
                            if all(key in processed_action_dict.keys() and processed_action_dict[key] != "" for key in ["name", "value"]):
                                if "type" in processed_action_dict.keys() and processed_action_dict["type"] == "str":
                                    processed_action_dict["value"] = f'"{processed_action_dict["value"]}"'

                                logic_elements.append(self.templates.set_variable_logic_template.render(action_dict=processed_action_dict))

        from inoft_vocal_framework.plugins.official_audio_files_instead_of_text import core as plugin_core
        plugin_core.execute(generator_core=self)

        for say_action in self.say_actions:
            if say_action.code is None:
                if say_action.message_item_to_say is not None:
                    say_action.code = f"{say_action.message_item_to_say.variable_name}.pick()"
                    say_action.is_callable = True
                else:
                    say_action.code = say_action.text_to_say_if_message_item_missing
                    say_action.is_callable = False

            logic_elements.append(self.templates.say_action_template.render(say_action=say_action, **say_action.extra_args))

        return logic_elements

    @staticmethod
    def write_to_file(text: str, filepath: str):
        with open(filepath, "w+", encoding="utf-8") as file:
            file.write(text)


class IntentNameCondition:
    CLASS_TYPE = "Condition"

    def __init__(self, intent_name: str):
        self.intent_name = intent_name
        self.class_name = to_class_name(self.intent_name)
        self.code = None

    def render(self, parent_core: GeneratorCore) -> list:
        self.code = parent_core.templates.intent_name_condition_template.render(class_name=self.class_name, intent_name=self.intent_name)
        return [self]

class StateHandler:
    CLASS_TYPE = "StateHandler"

    def __init__(self, node_name: str):
        self.cannot_include_else_statement = False
        self.counts_used_condition_intent_names = dict()
        self.node_name = node_name
        self.class_name = to_class_name(self.node_name)
        self.wait_for_user_response = True
        self.code = None
        self.next_paths = list()

    def set_cannot_include_else_statement(self, value: bool = True):
        self.cannot_include_else_statement = value
        return ""

    class Path:
        CONDITION_TYPE_INTENT_NAME = "intent_name"
        CONDITION_TYPE_ALWAYS = "always"
        CONDITION_TYPE_DATA = "data"

        def __init__(self, path_index: int, condition: str, target_node_name: str):
            self.path_index = path_index
            self.condition_str = condition
            self.condition_type = None
            self.condition_intent_name = None
            self.condition_data_key = None
            self.condition_statement = None
            self.target_node_name = target_node_name
            self.target_node_class = f"{to_class_name(target_node_name or '')}StateHandler"
            self.code_elements = list()

        def process(self, parent_core: GeneratorCore) -> bool:
            """:return Has empty code_elements and need to be removed from the paths list"""
            if self.target_node_name in parent_core.node_values_dict.keys():
                current_target_node_values_dict = parent_core.node_values_dict[self.target_node_name]
                storage_type_key = self.condition_str.split(".", maxsplit=1)[0]

                if self.condition_str is not None and "event.nlu.intent.name ===" in self.condition_str:
                    self.condition_type = self.CONDITION_TYPE_INTENT_NAME
                    self.condition_intent_name = to_class_name(self.condition_str.replace("event.nlu.intent.name ===", "")
                                                                   .replace(" ", "").replace("'", "").replace('"', ''))
                    self.code_elements = parent_core.process_on_enter(current_target_node_values_dict["onEnter"])

                elif self.condition_str == "true":
                    self.condition_type = self.CONDITION_TYPE_ALWAYS
                    self.code_elements = parent_core.process_on_enter(current_target_node_values_dict["onEnter"])

                elif any(key == storage_type_key for key in ["user", "session"]):
                    # todo: create a special handler function to retrieve data (or some default attributes that get a path)
                    self.condition_type = self.CONDITION_TYPE_DATA
                    self.condition_data_key, self.condition_statement = self.condition_str.split(" ", maxsplit=1)
                    self.condition_data_key = self.condition_data_key.replace(f"{storage_type_key}.", "")
                    self.code_elements = parent_core.process_on_enter(current_target_node_values_dict["onEnter"])

                else:
                    print(f"Warning ! Unsupported condition_type : {self.condition_str}")

                if not len(self.code_elements) > 0:
                    self.code_elements = None
                    return True
                else:
                    return False

    def process_paths(self, parent_core: GeneratorCore, paths: list) -> list:
        processed_paths = list()

        for i, path in enumerate(paths):
            path = SafeDict(path)
            path_condition = path.get("condition").to_str(default=None)
            path_target_node_name = path.get("node").to_str(default=None)

            if path_condition is not None and path_target_node_name is not None:
                current_path_instance = StateHandler.Path(path_index=i, condition=path_condition, target_node_name=path_target_node_name)
                no_code_generated_for_path = current_path_instance.process(parent_core=parent_core)
                if no_code_generated_for_path is False:
                    processed_paths.append(current_path_instance)
                else:
                    print(f"\nWarning ! The node {self.node_name} had a condition {path_condition} that did not generated any code.")
                    if path_target_node_name == "":
                        print("It is likely because you did not define a target node for this condition.")
                    else:
                        print(f"Yet you defined a target node. There is something fishy, you should look in botpress what is strange about the node {self.node_name}")

                if current_path_instance.condition_type == self.Path.CONDITION_TYPE_INTENT_NAME:
                    if current_path_instance.condition_intent_name in self.counts_used_condition_intent_names.keys():
                        self.counts_used_condition_intent_names[current_path_instance.condition_intent_name] += 1
                    else:
                        self.counts_used_condition_intent_names[current_path_instance.condition_intent_name] = 1

        return processed_paths

    def get_code(self, parent_core: GeneratorCore) -> str:
        if self.code is None:
            self.render(parent_core=parent_core)
        return self.code

    def process(self, parent_core: GeneratorCore):
        current_node_values_dict = parent_core.node_values_dict[self.node_name]
        on_receive = current_node_values_dict["onReceive"]
        self.wait_for_user_response = True if isinstance(on_receive, list) and len(on_receive) == 0 else False
        self.next_paths = self.process_paths(parent_core=parent_core, paths=(self.next_paths if len(self.next_paths) > 0 else current_node_values_dict["next"]))

    def render(self, parent_core: GeneratorCore) -> list:
        self.code = parent_core.templates.state_handler_template.render(class_name=self.class_name,
            node_name=self.node_name, wait_for_user_response=self.wait_for_user_response, paths=self.next_paths,
            counts_used_condition_intent_names=parent_core.counts_used_condition_intent_names,
            threshold_of_intent_use_to_create_a_condition=parent_core.threshold_of_intent_use_to_create_a_condition, cannot_include_else_statement=self.cannot_include_else_statement)
        return [self]

class LaunchRequestHandler:
    CLASS_TYPE = "RequestHandler"

    def __init__(self, node_dict: dict):
        self.node_safedict = SafeDict(node_dict)
        self.node_name = self.node_safedict.get("name").to_str()
        self.class_name = to_class_name(self.node_name)
        self.code = None
        self.state_handler_class = None

    def process(self, parent_core: GeneratorCore):
        next_paths = self.node_safedict.get("next").to_list()
        if len(next_paths) > 0:
            self.state_handler_class = StateHandler(node_name=self.node_name)
            for path in next_paths:
                self.state_handler_class.next_paths.append(path)  # all_nodes_classes_dict[next_paths[0]["name"]]

    def render(self, parent_core: GeneratorCore):  # dict, parent_all_nodes_classes_dict: dict):
        created_classes = list()

        next_state_handler_class = None
        if self.state_handler_class is not None:
            state_handler = StateHandler(node_name=self.node_name)
            state_handler.process(parent_core=parent_core)
            state_handler.render(parent_core=parent_core)
            created_classes.append(state_handler)
            next_state_handler_class = f"{self.class_name}StateHandler"

        self.code = parent_core.templates.launch_request_handler_template.render(class_name=self.class_name, node_name=self.node_name,
            next_state_handler_class=next_state_handler_class, code_elements=parent_core.process_on_enter(self.node_safedict.get("onEnter").to_list()))

        created_classes.insert(0, self)
        # We always want for the request handler to be the first element in the classes.
        return created_classes

# todo: fix issue with double node without text (for example ""node_name: node-bc35""")
class Messages:
    def __init__(self, messages_items: dict):
        self.input_messages_items = messages_items
        self.output_messages_dict: Dict[str, Messages.MessageItem] = dict()
        self.process()

    class MessageItem:
        def __init__(self, id_value: str = None, speech_items: list = None, is_callable: bool = False):
            self._id = id_value
            self.speechs = speech_items
            self.is_callable = is_callable
            self.variable_name = None
            self._update_variable_name()

        @property
        def id(self):
            return self._id

        @id.setter
        def id(self, id_value: str):
            self._id = id_value
            self._update_variable_name()

        def _update_variable_name(self):
            if isinstance(self.id, str):
                self.variable_name = "".join([char.capitalize() for char in self.id.replace("-", "_")])
            else:
                self.variable_name = None

    def process(self):
        for message_dict in self.input_messages_items:
            message_dict = SafeDict(message_dict)
            speech_items = list()

            # todo: make multilang (might require the premium version of botpress)
            main_speech_dict = message_dict.get("formData").to_dict()
            for key, value in main_speech_dict.items():
                if "text" in key:
                    if value is not None and value != "":
                        speech_items.append(prettify_speech_text(value))

                if "variations" in key:
                    if isinstance(value, list):
                        for speech_variation in value:
                            if speech_variation is not None and speech_variation != "":
                                speech_items.append(prettify_speech_text(value))

            message_item = self.MessageItem(id_value=message_dict.get("id").to_str(), speech_items=speech_items)
            self.output_messages_dict[message_item.id] = message_item

    def render(self, parent_core: GeneratorCore):
        code_messages_file = parent_core.templates.messages_template.render(messages=self.output_messages_dict.values())
        return code_messages_file

class SayAction:
    def __init__(self, message_id_to_say: str = None, message_item_to_say: Messages.MessageItem = None, is_callable: bool = False,
                 text_to_say_if_message_item_missing: Optional[str] = "A message element is missing.", code: str = None, extra_args: dict = None):

        self.message_id_to_say = message_id_to_say
        self.message_item_to_say = message_item_to_say
        self.is_callable = is_callable
        self.text_to_say_if_message_item_missing = text_to_say_if_message_item_missing
        self.code = code
        self.extra_args = extra_args if extra_args is not None else dict()

    @property
    def message_id_to_say(self) -> str:
        return self._message_id_to_say

    @message_id_to_say.setter
    def message_id_to_say(self, message_id_to_say: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=message_id_to_say, expected_type=str, variable_name="message_id_to_say")
        self._message_id_to_say = message_id_to_say

    @property
    def message_item_to_say(self) -> Messages.MessageItem:
        return self._message_item_to_say

    @message_item_to_say.setter
    def message_item_to_say(self, message_item_to_say: Messages.MessageItem) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=message_item_to_say, expected_type=Messages.MessageItem, variable_name="message_item_to_say")
        self._message_item_to_say = message_item_to_say

    @property
    def is_callable(self) -> bool:
        return self._is_callable

    @is_callable.setter
    def is_callable(self, is_callable: bool) -> None:
        raise_if_variable_not_expected_type(value=is_callable, expected_type=bool, variable_name="is_callable")
        self._is_callable = is_callable

    @property
    def text_to_say_if_message_item_missing(self) -> str:
        return self._text_to_say_if_message_item_missing

    @text_to_say_if_message_item_missing.setter
    def text_to_say_if_message_item_missing(self, text_to_say_if_message_item_missing: str) -> None:
        raise_if_variable_not_expected_type(value=text_to_say_if_message_item_missing, expected_type=str, variable_name="text_to_say_if_message_item_missing")
        self._text_to_say_if_message_item_missing = text_to_say_if_message_item_missing

    @property
    def code(self) -> str:
        return self._code

    @code.setter
    def code(self, code: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=code, expected_type=str, variable_name="code")
        self._code = code

    @property
    def extra_args(self) -> dict:
        return self._extra_args

    @extra_args.setter
    def extra_args(self, extra_args: dict) -> None:
        raise_if_variable_not_expected_type(value=extra_args, expected_type=dict, variable_name="extra_args")
        self._extra_args = extra_args

class SetVariableAction:
    def __init__(self):
        pass

if __name__ == "__main__":
    GeneratorCore(main_flow_filepath="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/botpress_integration/Scene_Sabotage.flow.json",
        builtin_text_filepath="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_framework/botpress_integration/builtin_text.json").process()
