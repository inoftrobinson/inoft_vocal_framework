import random


def safe_get_element_in_dict(dict_object: dict, key_to_get: str):
    if key_to_get in dict_object.keys():
        return dict_object[key_to_get]
    else:
        return None

def pick_one_randomly_from_list(list_to_pick_from: list):
    return list_to_pick_from[random.randint(0, len(list_to_pick_from) - 1)]

def pick_msg(speechs_list: list) -> str:
    if isinstance(speechs_list, list):
        if len(speechs_list) > 0:
            # I'm treating the probabilities so that in the data files,
            # i can simply use pseudo probabilities that do not add up to 1
            speech_texts = list()
            sum_probabilities = 0
            for speech_item in speechs_list:
                sum_probabilities += float(speech_item.probability_value)
                # Important to use float and not int
                speech_texts.append(speech_item.speech)

            probabilities_added_to_one = 0
            probabilities = list()
            for speech_item in speechs_list:
                probability_on_one = speech_item.probability_value / sum_probabilities
                probabilities.append(probability_on_one)
                probabilities_added_to_one += probability_on_one

            # We need for the probabilities to exactly sum up to one in order to work with numpy
            if probabilities_added_to_one > 0 and probabilities_added_to_one != 1 and len(probabilities) > 0:
                probability_to_remove_or_add_to_each_element = (probabilities_added_to_one - 1) / len(probabilities)
                for probability_value_of_element in probabilities:
                    probability_value_of_element += probability_to_remove_or_add_to_each_element

            picked_elements_list = random.choices(population=speech_texts, weights=probabilities)
            if picked_elements_list is not None and len(picked_elements_list) > 0:
                return picked_elements_list[0]
            else:
                return None
        else:
            raise Exception(f"No speech item are in the current speech list : {speechs_list}")
    else:
        raise Exception(f"The messages were not a list object but {speechs_list}")

def pick_msg_old(msgs) -> str:
    """ The key of a dict element is the message, and the value its probabilities """
    from inoft_vocal_engine.inoft_vocal_framework.speechs.ssml_builder_core import SpeechsList

    if isinstance(msgs, SpeechsList):
        msgs_dict = msgs.speechs_list
    elif isinstance(msgs, dict):
        msgs_dict = msgs
    else:
        raise Exception(f"The messages object was neither a SpeechsList or a dict but was {msgs}")

    if msgs_dict is not None:
        # I'm treating the probabilities so that in the data files,
        # i can simply use pseudo probabilities that do not add up to 1
        sum_probabilities = 0
        for probability_of_element in msgs_dict.values():
            sum_probabilities += float(probability_of_element)
            # Important to use float and not int

        probabilities_added_to_one = 0
        probabilities = list()
        for probability_of_element in msgs_dict.values():
            probability_on_one = probability_of_element / sum_probabilities
            probabilities.append(probability_on_one)
            probabilities_added_to_one += probability_on_one

        # We need for the probabilities to exactly sum up to one in order to work with numpy
        if probabilities_added_to_one > 0 and probabilities_added_to_one != 1 and len(probabilities) > 0:
            probability_to_remove_or_add_to_each_element = (probabilities_added_to_one - 1) / len(probabilities)
            for probability_value_of_element in probabilities:
                probability_value_of_element += probability_to_remove_or_add_to_each_element

        print(probabilities)
        picked_elements_list = random.choices(population=list(msgs_dict.keys()), weights=probabilities)
        if picked_elements_list is not None and len(picked_elements_list) > 0:
            return picked_elements_list[0]
        else:
            return None
    else:
        return "The variable send to the pick_msg was not in the form of a dict."
