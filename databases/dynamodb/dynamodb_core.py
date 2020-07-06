import logging

import boto3
from boto3.session import Session, ResourceNotExistsError

from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.utils.static_logger import logger

class DynamoDbCoreAdapter:
    _EXISTING_DATABASE_CLIENTS = dict()

    def __init__(self, table_name: str, region_name: str, primary_key_name="id", create_table=True):
        self.table_name = table_name
        self.primary_key_name = primary_key_name
        self.create_table = create_table

        self.utils = Utils()

        # We store the database clients in a static variable, so that if we init the class with
        # the same region_name, we do not need to wait for a new initialization of the client.
        if region_name in self._EXISTING_DATABASE_CLIENTS.keys():
            self.dynamodb = self._EXISTING_DATABASE_CLIENTS[region_name]
            print(f"Re-using the already created dynamodb client for region {region_name}")
        elif "default" in self._EXISTING_DATABASE_CLIENTS.keys():
            self.dynamodb = self._EXISTING_DATABASE_CLIENTS["default"]
            print(f"Re-using the already created dynamodb client for the default region")
        else:
            print(f"Initializing the {self}. For local development, make sure that you are connected to internet."
                  f"\nOtherwise the framework will get stuck at initializing the {self}")

            dynamodb_regions = Session().get_available_regions("dynamodb")
            if region_name in dynamodb_regions:
                self.dynamodb = boto3.client("dynamodb", region_name=region_name)
                self._EXISTING_DATABASE_CLIENTS[region_name] = self.dynamodb
            else:
                self.dynamodb = boto3.client("dynamodb")
                self._EXISTING_DATABASE_CLIENTS["default"] = self.dynamodb
                logger.debug(f"Warning ! The specified dynamodb region_name {region_name} is not a valid region_name."
                             f"The dynamodb client has been initialized without specifying the region.")

            self.__create_table_if_not_exists()
            print(f"Initialization of {self} completed successfully !")

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
                    BillingMode='PAY_PER_REQUEST',
                )
            except Exception as e:
                if e.__class__.__name__ != "ResourceInUseException":
                    raise Exception(f"Create table if not exists request failed: Exception of type {type(e).__name__} occurred {str(e)}")
