from boto3.exceptions import ResourceNotExistsError
from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter, PrimaryIndex
from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils


class AudioEditorProjectsDynamoDbClient(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name="projectId", hash_key_variable_python_type=str)
        super().__init__(table_name=table_name, region_name=region_name, primary_index=primary_index, create_table=True)

    def save_project_data(self, project_id: str, project_data: dict) -> bool:
        try:
            item = Utils.python_to_dynamodb(project_data)
            item["projectId"] = project_id
            print(f"Saving audio editor project data {item}")
            table = self.dynamodb.Table(self.table_name)
            table.put_item(Item=item)
            return True
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save project data to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def get_project_data_by_project_id(self, project_id: str) -> (dict, bool):
        # If the value from get_field is of dict or list type, the SafeDict will be populated, otherwise it will be empty without errors.
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={"projectId": project_id}, ConsistentRead=True)
            if "Item" in response:
                # Utils.decimal_deserializer(
                return Utils.dynamodb_to_python(response["Item"]), True
            else:
                return dict(), False
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")
