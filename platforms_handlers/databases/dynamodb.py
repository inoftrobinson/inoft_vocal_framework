import boto3
from ask_sdk_core.exceptions import PersistenceException
from ask_sdk_dynamodb.partition_keygen import user_id_partition_keygen
from boto3.session import Session, ResourceNotExistsError

from inoft_vocal_framework.utils.static_logger import logger


class DynamoDbAdapter:
    """Persistence Adapter implementation using Amazon DynamoDb.

    Amazon DynamoDb based persistence adapter implementation. This
    internally uses the AWS Python SDK (`boto3`) to process the
    dynamodb operations. The adapter tries to create the table if
    ``create_table`` is set, during initialization.

    :param table_name: Name of the table to be created or used
    :type table_name: str
    :param primary_key_name: Partition key name to be used.
        Defaulted to 'id'
    :type primary_key_name: str
    :param attribute_name: Attribute name for storing and
        retrieving attributes from dynamodb.
        Defaulted to 'attributes'
    :type attribute_name: str
    :param create_table: Should the adapter try to create the table
        if it doesn't exist. Defaulted to False
    :type create_table: bool
    :param partition_keygen: Callable function that takes a
        request envelope and provides a unique partition key value.
        Defaulted to user id keygen function
    :type partition_keygen: Callable[[RequestEnvelope], str]
    """

    def __init__(self, table_name: str, region_name: str, primary_key_name="id", attribute_name="attributes",
                 create_table=True, partition_keygen=user_id_partition_keygen):
        """Persistence Adapter implementation using Amazon DynamoDb.

        Amazon DynamoDb based persistence adapter implementation. This
        internally uses the AWS Python SDK (`boto3`) to process the
        dynamodb operations. The adapter tries to create the table if
        `create_table` is set, during initialization.

        :param table_name: Name of the table to be created or used
        :type table_name: str
        :param primary_key_name: Partition key name to be used. Defaulted to 'id'
        :type primary_key_name: str
        :param attribute_name: Attribute name for storing and retrieving attributes from dynamodb. Defaulted to 'attributes'
        :type attribute_name: str
        :param create_table: Should the adapter try to create the table if it doesn't exist. Defaulted to False
        :type create_table: bool
        :param partition_keygen: Callable function that takes a request envelope and provides a unique partition key value. Defaulted to user id keygen function
        :type partition_keygen: Callable[[RequestEnvelope], str]
        """
        print(f"Initializing the {self}. For local development, make sure that you are connected to internet."
              f"Otherwise the framework will get stuck at initializing the {self}")

        self._user_id = None
        self.table_name = table_name
        self.primary_key_name = primary_key_name
        self.attribute_name = attribute_name
        self.create_table = create_table
        self.partition_keygen = partition_keygen

        dynamodb_regions = Session().get_available_regions("dynamodb")
        if region_name in dynamodb_regions:
            self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        else:
            self.dynamodb = boto3.resource("dynamodb")
            logger.debug(f"Warning ! The specified dynamodb region_name {region_name} is not a valid region_name."
                         f"The dynamodb client has been initialized without specifying the region.")

        self.__create_table_if_not_exists()
        print(f"Initialization of {self} completed successfully !")

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str) -> None:
        if not isinstance(user_id, str):
            raise Exception(f"user_id was type {type(user_id)} which is not valid value for his parameter.")
        elif user_id.replace(" ", "") == "":
            raise Exception(f"user_id was of type {type(user_id)} but cannot be empty and was : '{user_id}'")
        self._user_id = user_id

    # todo: create an option of bandwith optimization by loading the
    #  persistent attributes in the session attributes at the start of the session

    # todo: make work the retrieving/saving of attributes when deployed to the cloud (currently work in local but not in the cloud)
    def get_attributes(self, user_id: str) -> dict:
        """ Get attributes from table in Dynamodb resource.

        Retrieves the attributes from Dynamodb table. If the table
        doesn't exist, returns an empty dict if the
        ``create_table`` variable is set as True, else it raises
        PersistenceException. Raises PersistenceException if `get_item`
        fails on the table.

        :return: Attributes stored under the partition keygen mapping in the table
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={"id": user_id}, ConsistentRead=True)
            if "Item" in response:
                return response["Item"][self.attribute_name]
            else:
                return {}
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} do not exist or in the process of "
                                       f"being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to retrieve attributes from DynamoDb table. "
                                       f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def save_attributes(self, attributes: dict) -> None:
        """ Saves attributes to table in Dynamodb resource.

        Saves the attributes into Dynamodb table. Raises
        PersistenceException if table doesn't exist or ``put_item`` fails
        on the table.

        :param attributes: Attributes stored under the partition keygen mapping in the table
        """
        print(f"Saving persistent attributes to user_id {self.user_id} : {attributes}")
        try:
            table = self.dynamodb.Table(self.table_name)
            table.put_item(Item={"id": self.user_id, self.attribute_name: attributes})
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, request_envelope):
        """Deletes attributes from table in Dynamodb resource.

        Deletes the attributes from Dynamodb table. Raises
        PersistenceException if table doesn't exist or ``delete_item`` fails
        on the table.

        :param request_envelope: Request Envelope passed during skill
            invocation
        :type request_envelope: ask_sdk_model.RequestEnvelope
        :rtype: None
        :raises: :py:class:`ask_sdk_core.exceptions.PersistenceException`
        """
        try:
            table = self.dynamodb.Table(self.table_name)
            partition_key_val = self.partition_keygen(request_envelope)
            table.delete_item(Key={self.primary_key_name: partition_key_val})
        except ResourceNotExistsError:
            raise PersistenceException(f"DynamoDb table {self.table_name} doesn't exist. Failed to delete attributes from DynamoDb table.")
        except Exception as e:
            raise PersistenceException(f"Failed to delete attributes in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def __create_table_if_not_exists(self) -> None:
        """
        Creates table in Dynamodb resource if it doesn't exist and create_table is set as True.
        :rtype: None
        :raises: PersistenceException: When `create_table` fails on
            dynamodb resource.
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
