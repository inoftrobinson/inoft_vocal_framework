import time

import boto3
from ask_sdk_core.exceptions import PersistenceException
from boto3.dynamodb.table import TableResource
from boto3.session import Session, ResourceNotExistsError

from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.static_logger import logger


class DynamoDbAdapter:
    """Persistence Adapter implementation using Amazon DynamoDb.

    Amazon DynamoDb based persistence adapter implementation. This
    internally uses the AWS Python SDK (`boto3`) to process the
    dynamodb operations. The adapter tries to create the table if
    ``create_table`` is set, during initialization.

    :param table_name: Name of the table to be created or used
    :type table_name: str
    :param primary_key_name: Partition key name to be used. Defaulted to 'id'
    :type primary_key_name: str
    :param create_table: Should the adapter try to create the table if it doesn't exist. Defaulted to False
    :type create_table: bool
    :param persistent_attributes_key_name: Attribute name for storing and retrieving attributes from dynamodb. Defaulted to 'attributes'
    :type persistent_attributes_key_name: str
    """

    def __init__(self, table_name: str, region_name: str, primary_key_name="id", create_table=True,
                 persistent_attributes_key_name="persistent_attributes",
                 smart_session_attributes_key_name="smart_session_attributes"):
        """Persistence Adapter implementation using Amazon DynamoDb.

        Amazon DynamoDb based persistence adapter implementation. This
        internally uses the AWS Python SDK (`boto3`) to process the
        dynamodb operations. The adapter tries to create the table if
        `create_table` is set, during initialization.

        :param table_name: Name of the table to be created or used
        :type table_name: str
        :param primary_key_name: Partition key name to be used. Defaulted to 'id'
        :type primary_key_name: str
        :param persistent_attributes_key_name: Attribute name for storing and retrieving attributes from dynamodb. Defaulted to 'attributes'
        :type persistent_attributes_key_name: str
        :param create_table: Should the adapter try to create the table if it doesn't exist. Defaulted to False
        :type create_table: bool
        """
        print(f"Initializing the {self}. For local development, make sure that you are connected to internet."
              f"\nOtherwise the framework will get stuck at initializing the {self}")

        self.table_name = table_name
        self.primary_key_name = primary_key_name
        self.create_table = create_table
        self.persistent_attributes_key_name = persistent_attributes_key_name
        self.smart_session_attributes_key_name = smart_session_attributes_key_name

        dynamodb_regions = Session().get_available_regions("dynamodb")
        if region_name in dynamodb_regions:
            self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        else:
            self.dynamodb = boto3.resource("dynamodb")
            logger.debug(f"Warning ! The specified dynamodb region_name {region_name} is not a valid region_name."
                         f"The dynamodb client has been initialized without specifying the region.")

        self.__create_table_if_not_exists()
        print(f"Initialization of {self} completed successfully !")
        self._fetchedData = None
        self._last_user_id = None

    # todo: create an option of bandwith optimization by loading the
    #  persistent attributes in the session attributes at the start of the session

    def _fetch_attributes(self, user_id: str) -> SafeDict:
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={"id": user_id}, ConsistentRead=True)
            if "Item" in response:
                from inoft_vocal_framework.platforms_handlers.databases.dynamodb_utils import dynamodb_to_dict
                return SafeDict(dynamodb_to_dict(response["Item"]))
            else:
                return SafeDict()
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} do not exist or in the process of "
                                       f"being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to retrieve attributes from DynamoDb table. "
                                       f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def _get_db_table(self):
        # todo: find what type of object is a dynamodb Table (if any)
        return self.dynamodb.Table(self.table_name)

    @property
    def fetchedData(self) -> SafeDict:
        if self._fetchedData is None:
            self._fetchedData = self._fetch_attributes(user_id=self.last_user_id)
        return self._fetchedData

    def get_field(self, user_id: str, field_key: str):
        self.last_user_id = user_id
        return self.fetchedData.get(field_key).to_any()

    def get_smart_session_attributes(self, user_id: str, session_id: str, timeout_seconds: int) -> (SafeDict, bool):
        # If the value from get_field is of dict or list type, the SafeDict will be populated, otherwise it will be empty without errors.
        timeout_expired = True

        last_session_id = self.get_field(user_id=user_id, field_key="lastSessionId")
        if session_id == last_session_id:
            timeout_expired = False
        else:
            last_interaction_time = self.get_field(user_id=user_id, field_key="lastInteractionTime")
            if last_interaction_time is not None and time.time() <= last_interaction_time + timeout_seconds:
                timeout_expired = False

        if timeout_expired is False:
            return SafeDict(self.get_field(user_id=user_id, field_key=self.smart_session_attributes_key_name)), True
        else:
            return SafeDict(), False

    #todo: make it so that the smart session data timeout can be customized for each user, and is saved and retrieved from the db at each invocation
    def get_persistent_attributes(self, user_id: str) -> SafeDict:
        # If the value from get_field is of dict or list type, the SafeDict will be populated, otherwise it will be empty without errors.
        return SafeDict(self.get_field(user_id=user_id, field_key=self.persistent_attributes_key_name))

    def save_attributes(self, user_id: str, session_id: str, smart_session_attributes: dict, persistent_attributes: dict) -> None:
        self.last_user_id = user_id

        if not isinstance(smart_session_attributes, dict):
            print(f"smart_session_attributes has been set to empty dict because was not of dict type but {smart_session_attributes}")
            smart_session_attributes = dict()
        if not isinstance(persistent_attributes, dict):
            print(f"persistent_attributes has been set to empty dict because was not of dict type but {persistent_attributes}")
            persistent_attributes = dict()

        item_dict = {
            "id": user_id,
            "lastSessionId": session_id,
            "lastInteractionTime": round(time.time()),  # No need to store milliseconds for the last interaction time
            self.smart_session_attributes_key_name: smart_session_attributes,
            self.persistent_attributes_key_name: persistent_attributes
        }

        try:
            print(f"Saving attributes : {item_dict}")
            table = self._get_db_table()
            from inoft_vocal_framework.platforms_handlers.databases.dynamodb_utils import dict_to_dynamodb
            out = dict_to_dynamodb(item_dict)
            table.put_item(Item=dict_to_dynamodb(item_dict))
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, user_id: str):
        """ Deletes attributes from table in Dynamodb resource. """
        self.last_user_id = user_id
        try:
            table = self._get_db_table()
            table.delete_item(Key={self.primary_key_name: user_id})
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} doesn't exist. Failed to delete attributes from DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to delete attributes in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

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

    @property
    def last_user_id(self) -> str:
        return self._last_user_id

    @last_user_id.setter
    def last_user_id(self, last_user_id: str) -> None:
        if not isinstance(last_user_id, str):
            raise Exception(f"last_user_id was type {type(last_user_id)} which is not valid value for his parameter.")
        self._last_user_id = last_user_id
