import boto3
from boto3.session import Session, ResourceNotExistsError
from inoft_vocal_framework.utils.static_logger import logger

class DynamoDbCoreAdapter:
    def __init__(self, table_name: str, region_name: str, primary_key_name="id", create_table=True):
        print(f"Initializing the {self}. For local development, make sure that you are connected to internet."
              f"\nOtherwise the framework will get stuck at initializing the {self}")

        self.table_name = table_name
        self.primary_key_name = primary_key_name
        self.create_table = create_table

        dynamodb_regions = Session().get_available_regions("dynamodb")
        if region_name in dynamodb_regions:
            self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        else:
            self.dynamodb = boto3.resource("dynamodb")
            logger.debug(f"Warning ! The specified dynamodb region_name {region_name} is not a valid region_name."
                         f"The dynamodb client has been initialized without specifying the region.")

        self.__create_table_if_not_exists()
        print(f"Initialization of {self} completed successfully !")

    def _get_db_table(self):
        # todo: find what type of object is a dynamodb Table (if any)
        return self.dynamodb.Table(self.table_name)

    def __create_table_if_not_exists(self) -> None:
        """
        Creates table in Dynamodb resource if it doesn't exist and create_table is set as True.
        :raises: PersistenceException: When `create_table` fails on dynamodb resource.
        """
        if self.create_table:
            try:
                self.dynamodb.create_table(
                    TableName=self.table_name,
                    KeySchema=[
                        {
                            'AttributeName': self.primary_key_name,
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': self.primary_key_name,
                            'AttributeType': 'S'
                        }
                    ],
                    ProvisionedThroughput={
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                )
            except Exception as e:
                if e.__class__.__name__ != "ResourceInUseException":
                    raise Exception(f"Create table if not exists request failed: Exception of type {type(e).__name__} occurred {str(e)}")