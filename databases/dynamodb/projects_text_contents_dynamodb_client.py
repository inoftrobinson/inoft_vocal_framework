from typing import Optional, Any, List
from boto3.dynamodb.conditions import Key
from boto3.exceptions import ResourceNotExistsError
from pydantic import BaseModel

from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter, GlobalSecondaryIndex, PrimaryIndex, \
    Response
from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.inoft_vocal_markup.deserializer import DialogueLine


class ContentItem(BaseModel):
    elementId: str
    creationTimestamp: int
    lastModificationTimestamp: int
    sectionInstanceId: int
    stateId: int
    dialogueLines: Optional[List[DialogueLine]] = None

class ProjectsTextContentsDynamoDbClient(DynamoDbCoreAdapter):
    """
    State Ids :
    -2 = Deleted but stored
    -1 = Archived, and will not be classically displayed
    0 = Available in the standard interface
    """

    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name="elementId", hash_key_variable_python_type=str)

        globals_secondary_indexes = [
            # GlobalSecondaryIndex(index_name="characterNames", key_type=GlobalSecondaryIndex.KEY_TYPE_IS_HASH_KEY,
            #                     variable_python_type=list, projection_type=GlobalSecondaryIndex.PROJECTION_TYPE_USE_ALL),
            # I cannot have a sort key be a list, so i guess to get all the content that include a character, with a scan query :/
            GlobalSecondaryIndex(hash_key_name="sectionInstanceId", hash_key_variable_python_type=int,
                                 sort_key_name="creationTimestamp", sort_key_variable_python_type=int,
                                 projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="sectionInstanceId", hash_key_variable_python_type=int,
                                 sort_key_name="lastModificationTimestamp", sort_key_variable_python_type=int,
                                 projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="stateId", hash_key_variable_python_type=int,
                                 sort_key_name="creationTimestamp", sort_key_variable_python_type=int,
                                 projection_type="ALL"),
            GlobalSecondaryIndex(hash_key_name="stateId", hash_key_variable_python_type=int,
                                 sort_key_name="lastModificationTimestamp", sort_key_variable_python_type=int,
                                 projection_type="ALL")
        ]
        super().__init__(table_name=table_name, region_name=region_name, primary_index=primary_index,
                         create_table=True, global_secondary_indexes=globals_secondary_indexes)

    def put_new_content(self, db_item: ContentItem):
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(Item=db_item.dict())
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def update_content_element(self, element_id: str, dialogue_line_index: int, element_text: str) -> Response:
        # todo: add support for dialogue line, because currently we are replacing the lines by a single text
        try:
            table = self.dynamodb.Table(self.table_name)
            dialogue_line = DialogueLine(character_name="Default", line_content=element_text, additional_character_metadata=None)
            # Todo: add support for character name and additional character metadata

            from time import time
            response = table.update_item(
                Key={"elementId": element_id},
                UpdateExpression=f"SET dialogueLines[{dialogue_line_index}]=:dialogueLine, lastModificationTimestamp=:timestamp",
                ExpressionAttributeValues={
                    ':dialogueLine': dialogue_line.dict(),
                    ":timestamp": round(time())
                    # We need the timestamp to be an int, not a float, so we round it.
                },
                ReturnValues="UPDATED_NEW"
            )
            print(response)
            return response

        except ResourceNotExistsError:
            raise Exception( f"DynamoDb table {self.table_name} doesn't exist. Failed to update attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to update attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def _get_latest(self, index_name: str, num_latest_items: int, exclusive_start_key: Optional[dict] = None) -> Response:
        query = {
            "TableName": self.table_name,
            "IndexName": index_name,
            "KeyConditionExpression": Key("stateId").eq(0),
            "ScanIndexForward": False,
            "Limit": num_latest_items
        }
        if exclusive_start_key is not None:
            query["ExclusiveStartKey"] = exclusive_start_key

        table = self.dynamodb.Table(self.table_name)
        response = table.query(**query)
        print(response)
        # We use a scan instead of a query, since we just want the latest items without any conditions.
        if "Items" in response:
            return Response(Utils.dynamodb_to_python(dynamodb_object=response))  # , text_decoding_type="utf-8"))
            # todo: check if there are no issues when i do not specify the text decoding type
        else:
            return Response({})

    def get_latest_created(self, num_latest_items: int, exclusive_start_key: Optional[dict] = None) -> Response:
        return self._get_latest(index_name="stateId-creationTimestamp",
                                num_latest_items=num_latest_items, exclusive_start_key=exclusive_start_key)

    def get_latest_updated(self, num_latest_items: int, exclusive_start_key: Optional[dict] = None) -> Response:
        return self._get_latest(index_name="stateId-lastModificationTimestamp",
                                num_latest_items=num_latest_items, exclusive_start_key=exclusive_start_key)

    """
    def put_item(self, project_data: dict) -> bool:
        try:
            print(f"Saving project data {project_data}")
            item = Utils.python_to_dynamodb(project_data)
            self.dynamodb.put_item(TableName=self.table_name, Item=item)
            return True
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save project data to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")
        
    def get_project_data_by_project_id(self, project_id: str) -> (dict, bool):
        # If the value from get_field is of dict or list type, the SafeDict will be populated, otherwise it will be empty without errors.
        try:
            response = self.dynamodb.get_item(TableName=self.table_name,
                                              Key={"projectId": self.utils.python_to_dynamodb(project_id)},
                                              ConsistentRead=True)
            if "Item" in response:
                return self.utils.decimal_deserializer(self.utils.dynamodb_to_python(response["Item"])), True
            else:
                return dict(), False
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")
    """


if __name__ == "__main__":
    projects_text_contents_dynamodb_static_client = ProjectsTextContentsDynamoDbClient(
        table_name="test-inoft-vocal-engine-project-text-contents", region_name="eu-west-2"
    )
    data = projects_text_contents_dynamodb_static_client.get_latest_updated(num_latest_items=3).items
