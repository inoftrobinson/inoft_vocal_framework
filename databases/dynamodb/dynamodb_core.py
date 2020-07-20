from decimal import Decimal

import boto3
from boto3.session import Session
from typing import List, Optional, Type

from pydantic import BaseModel, StrictStr, validate_arguments

from inoft_vocal_engine.databases.dynamodb.dynamodb_utils import Utils
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.utils.static_logger import logger

HASH_KEY_TYPE = "HASH"
SORT_KEY_TYPE = "RANGE"


class Response:
    def __init__(self, response_dict: dict):
        response_safedict = SafeDict(response_dict)
        self.items = response_safedict.get("Items").to_list(default=None)
        self.count = response_safedict.get("Count").to_int(default=None)
        self.scanned_count = response_safedict.get("ScannedCount").to_int(default=None)
        self.last_evaluated_key = response_safedict.get("LastEvaluatedKey").to_dict(default=None)
        self.has_reached_end = False if self.last_evaluated_key is not None else True

class Index(BaseModel):
    hash_key_name: str
    hash_key_variable_python_type: Type
    sort_key_name: Optional[str]
    sort_key_variable_python_type: Optional[Type]
    index_custom_name: Optional[str]

class PrimaryIndex(Index):
    pass

class GlobalSecondaryIndex(Index):
    # todo: add pydantic to this class
    PROJECTION_TYPE_USE_ALL = "ALL"
    PROJECTION_TYPE_KEYS_ONLY = "KEYS_ONLY"
    PROJECTION_TYPE_INCLUDE = "INCLUDE"
    ALL_PROJECTIONS_TYPES = [PROJECTION_TYPE_USE_ALL, PROJECTION_TYPE_KEYS_ONLY, PROJECTION_TYPE_INCLUDE]

    projection_type: str

    def __init__(self, hash_key_name: str, hash_key_variable_python_type: Type,
                 sort_key_name: Optional[str], sort_key_variable_python_type: Optional[Type], projection_type: str,
                 index_custom_name: Optional[str] = None):

        super().__init__(hash_key_name=hash_key_name, hash_key_variable_python_type=hash_key_variable_python_type,
                         sort_key_name=sort_key_name, sort_key_variable_python_type=sort_key_variable_python_type,
                         projection_type=projection_type)

        if projection_type not in self.ALL_PROJECTIONS_TYPES:
            raise Exception(f"{projection_type} has not been found in the available projection_types : {self.ALL_PROJECTIONS_TYPES}")
        self.projection_type = projection_type

    def to_dict(self):
        if self.index_custom_name is not None:
            index_name = self.index_custom_name
        else:
            if self.sort_key_name is None:
                index_name = self.hash_key_name
            else:
                index_name = f"{self.hash_key_name}-{self.sort_key_name}"

        output_dict = {
            "IndexName": index_name,
            "KeySchema": [
                {
                    "AttributeName": self.hash_key_name,
                    "KeyType": HASH_KEY_TYPE
                },
            ],
            "Projection": {
                "ProjectionType": self.projection_type
            }
        }
        if self.sort_key_name is not None and self.sort_key_variable_python_type is not None:
            output_dict["KeySchema"].append({
                "AttributeName": self.sort_key_name,
                "KeyType": SORT_KEY_TYPE
            })
        return output_dict


class CreateTableQueryKwargs:
    @validate_arguments
    def __init__(self, table_name: str, billing_mode: str):
        self._names_already_defined_attributes: List[str] = list()
        self.data = {
            "TableName": table_name,
            "KeySchema": list(),
            "AttributeDefinitions": list(),
            "BillingMode": billing_mode,
        }

    def _add_key(self, key_name: str, key_python_variable_type: Type, key_type: str):
        self.data["KeySchema"].append({
            "AttributeName": key_name,
            "KeyType": key_type
        })
        self.data["AttributeDefinitions"].append({
            "AttributeName": key_name,
            "AttributeType": Utils.python_type_to_dynamodb_type(python_type=key_python_variable_type)
        })

    @validate_arguments
    def add_hash_key(self, key_name: str, key_python_variable_type: Type):
        self._add_key(key_name=key_name, key_python_variable_type=key_python_variable_type, key_type=HASH_KEY_TYPE)

    @validate_arguments
    def add_sort_key(self, key_name: str, key_python_variable_type: Type):
        self._add_key(key_name=key_name, key_python_variable_type=key_python_variable_type, key_type=SORT_KEY_TYPE)

    def _add_global_secondary_index(self, key_name: str, key_python_variable_type: Type):
        if key_name not in self._names_already_defined_attributes:
            self.data["AttributeDefinitions"].append({
                "AttributeName": key_name,
                "AttributeType": Utils.python_type_to_dynamodb_type(python_type=key_python_variable_type)
            })
            self._names_already_defined_attributes.append(key_name)

    @validate_arguments
    def add_global_secondary_index(self, global_secondary_index: GlobalSecondaryIndex):
        if "GlobalSecondaryIndexes" not in self.data:
            self.data["GlobalSecondaryIndexes"] = list()

        self._add_global_secondary_index(key_name=global_secondary_index.hash_key_name,
                                         key_python_variable_type=global_secondary_index.hash_key_variable_python_type)
        if global_secondary_index.sort_key_name is not None and global_secondary_index.sort_key_variable_python_type is not None:
            self._add_global_secondary_index(key_name=global_secondary_index.sort_key_name,
                                             key_python_variable_type=global_secondary_index.sort_key_variable_python_type)

        self.data["GlobalSecondaryIndexes"].append(global_secondary_index.to_dict())

    @validate_arguments
    def add_all_global_secondary_indexes(self, global_secondary_indexes: List[GlobalSecondaryIndex]):
        for global_secondary_index in global_secondary_indexes:
            self.add_global_secondary_index(global_secondary_index=global_secondary_index)


if __name__ == "__main__":
    c = CreateTableQueryKwargs(table_name="test", billing_mode="e")
    c.add_hash_key(key_name="t", key_python_variable_type=int)


class DynamoDbCoreAdapter:
    _EXISTING_DATABASE_CLIENTS = dict()
    PAY_PER_REQUEST = "PAY_PER_REQUEST"
    PROVISIONED = "PROVISIONED"

    def __init__(self, table_name: str, region_name: str, primary_index: PrimaryIndex,
                 create_table: bool = True, billing_mode: str = PAY_PER_REQUEST,
                 global_secondary_indexes: List[GlobalSecondaryIndex] = None):
        self.table_name = table_name
        self.primary_index = primary_index
        self.create_table = create_table
        self.billing_mode = billing_mode
        self.global_secondary_indexes = global_secondary_indexes

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
                self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
                self._EXISTING_DATABASE_CLIENTS[region_name] = self.dynamodb
            else:
                self.dynamodb = boto3.resource("dynamodb")
                self._EXISTING_DATABASE_CLIENTS["default"] = self.dynamodb
                logger.debug(f"Warning ! The specified dynamodb region_name {region_name} is not a valid region_name."
                             f"The dynamodb client has been initialized without specifying the region.")

        self._create_table_if_not_exists()
        print(f"Initialization of {self} completed successfully !")

    def _create_table_if_not_exists(self) -> None:
        """
        Creates table in Dynamodb resource if it doesn't exist and create_table is set as True.
        :raises: PersistenceException: When `create_table` fails on dynamodb resource.
        """
        if self.create_table:
            create_table_query_kwargs = CreateTableQueryKwargs(table_name=self.table_name, billing_mode=self.billing_mode)

            create_table_query_kwargs.add_hash_key(key_name=self.primary_index.hash_key_name,
                                                   key_python_variable_type=self.primary_index.hash_key_variable_python_type)

            if self.primary_index.sort_key_name is not None and self.primary_index.sort_key_variable_python_type is not None:
                create_table_query_kwargs.add_hash_key(key_name=self.primary_index.sort_key_name,
                                                       key_python_variable_type=self.primary_index.sort_key_variable_python_type)

            if self.global_secondary_indexes is not None:
                create_table_query_kwargs.add_all_global_secondary_indexes(global_secondary_indexes=self.global_secondary_indexes)
            try:
                print(create_table_query_kwargs.data)
                self.dynamodb.create_table(**create_table_query_kwargs.data)
            except Exception as e:
                if e.__class__.__name__ != "ResourceInUseException":
                    raise Exception(f"Create table if not exists request failed: Exception of type {type(e).__name__} occurred {str(e)}")


