from typing import List

from inoft_vocal_engine.cli.botpress.content_element_object import ContentElement
from inoft_vocal_engine.safe_dict import SafeDict


def get_list_content(filepath: str) -> List[ContentElement]:
    from inoft_vocal_engine.utils.general import load_json
    list_all_text_elements = load_json(filepath)

    from inoft_vocal_engine.inoft_vocal_markup.deserializer import Deserializer
    inoft_vocal_markup_deserializer = Deserializer(characters_names=["Léo", "Willie", "Menu"])

    content_elements: List[ContentElement] = list()
    for text_element in list_all_text_elements:
        current_content_element = ContentElement()

        text_element_safedict = SafeDict(text_element)
        text_content = text_element_safedict.get("formData").get("text$fr").to_str(default=None)
        if text_content is not None:
            current_content_element.dialogues_lines = inoft_vocal_markup_deserializer.deserialize(text=text_content)
            # todo: give the ability to select the language to deserialize

        current_content_element.id = text_element_safedict.get("id").to_str(default=None)
        current_content_element.created_by = text_element_safedict.get("createdBy").to_str(default=None)
        current_content_element.created_on = text_element_safedict.get("createdOn").to_str(default=None)
        current_content_element.modified_on = text_element_safedict.get("modifiedOn").to_str(default=None)
        content_elements.append(current_content_element)

    return content_elements
