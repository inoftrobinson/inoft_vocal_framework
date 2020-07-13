from boto3.exceptions import ResourceNotExistsError

from inoft_vocal_engine.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter
from inoft_vocal_engine.safe_dict import SafeDict


class AudioEditorProjectsDynamoDbClient(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str, primary_key_name="projectId", create_table=True):
        super().__init__(table_name=table_name, region_name=region_name, primary_key_name=primary_key_name, create_table=create_table)

    def save_project_data(self, project_data: dict) -> bool:
        try:
            print(f"Saving project data {project_data}")
            self.item = self.utils.python_to_dynamodb(project_data)
            self.dynamodb.put_item(TableName=self.table_name, Item=self.item)
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
