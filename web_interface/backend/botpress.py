from datetime import datetime
from typing import List
from inoft_vocal_engine.cli.botpress.content_element_object import ContentElement
from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ProjectsTextContentsDynamoDbClient
from inoft_vocal_engine.safe_dict import SafeDict


def botpress_content_to_list_content_elements(filepath: str) -> List[ContentElement]:
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

def botpress_date_to_timestamp(date_string: str) -> int:
    return round(datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp())

def put_new_botpress_content(filepath: str, projects_text_contents_dynamodb_client: ProjectsTextContentsDynamoDbClient):
    # filepath = "F:/Inoft/anvers_1944_project/inoft_vocal_engine/botpress_integration/builtin_text.json"
    list_content = botpress_content_to_list_content_elements(filepath=filepath)
    for content in list_content:
        from inoft_vocal_engine.databases.dynamodb.projects_text_contents_dynamodb_client import ContentItem
        db_item = ContentItem(elementId=content.id, sectionInstanceId=12, stateId=0,
                              creationTimestamp=botpress_date_to_timestamp(content.created_on),
                              lastModificationTimestamp=botpress_date_to_timestamp(content.modified_on),
                              dialogueLines=content.dialogues_lines)
        projects_text_contents_dynamodb_client.put_new_content(db_item)
