import time
from typing import Optional
from boto3.session import ResourceNotExistsError
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type
from inoft_vocal_framework.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.speechs.ssml_builder_core import Speech, SpeechsList


class DynamoDbAttributesAdapter(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str, primary_key_name="id", create_table=True,
                 persistent_attributes_key_name="persistentAttributes", smart_session_attributes_key_name="smartSessionAttributes"):
        super().__init__(table_name=table_name, region_name=region_name)

        self.persistent_attributes_key_name = persistent_attributes_key_name
        self.smart_session_attributes_key_name = smart_session_attributes_key_name

        self._fetchedData = None
        self._last_user_id = None

    # todo: create an option of bandwith optimization by loading the
    #  persistent attributes in the session attributes at the start of the session

    def _fetch_attributes(self, user_id: str) -> SafeDict:
        try:
            response = self.dynamodb.get_item(TableName=self.table_name, Key={"id": self.utils.python_to_dynamodb(user_id)}, ConsistentRead=True)
            if "Item" in response:
                return SafeDict(self.utils.dynamodb_to_python(response["Item"]))
            else:
                return SafeDict()
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process"
                            "of being created. Failed to get attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve attributes from DynamoDb table."
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")

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

    # todo: make it so that the smart session data timeout can be customized for each user, and is saved and retrieved from the db at each invocation
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
            self.dynamodb.put_item(TableName=self.table_name, Item=self.utils.python_to_dynamodb(item_dict))
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, user_id: str):
        """ Deletes attributes from table in Dynamodb resource. """
        self.last_user_id = user_id
        try:
            self.dynamodb.delete_item(TableName=self.table_name, Key={self.primary_key_name: user_id})
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to delete attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to delete attributes in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    @property
    def last_user_id(self) -> str:
        return self._last_user_id

    @last_user_id.setter
    def last_user_id(self, last_user_id: str) -> None:
        if not isinstance(last_user_id, str):
            raise Exception(f"last_user_id was type {type(last_user_id)} which is not valid value for his parameter.")
        self._last_user_id = last_user_id


class DynamoDbMessagesAdapter(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str, is_admin_mode=False,
                 persistent_attributes_key_name="persistentAttributes", smart_session_attributes_key_name="smartSessionAttributes"):
        super().__init__(table_name=table_name, region_name=region_name)

        self.persistent_attributes_key_name = persistent_attributes_key_name
        self.smart_session_attributes_key_name = smart_session_attributes_key_name

        self.is_admin_mode = is_admin_mode
        self._last_fetched_messages_list = None
        self._last_messages_list_id = None

    def _speech_dicts_to_speech_items(self, speech_dicts: list) -> list:
        output_list = list()
        for speech_dict in speech_dicts:
            output_list.append(Speech().from_dict(speech_safedict=SafeDict(speech_dict)))
        return output_list

    def get_fetched_messages_list(self, messages_list_id: str) -> list:
        if self._last_fetched_messages_list is None or messages_list_id != self.last_messages_list_id:
            try:
                response = self.dynamodb.get_item(TableName=self.table_name, Key={"id": self.utils.python_to_dynamodb(messages_list_id)}, ConsistentRead=True)
                if "Item" in response and "speechItems" in response["Item"]:
                    self._last_fetched_messages_list = self._speech_dicts_to_speech_items(self.utils.dynamodb_to_python(response["Item"]["speechItems"]))
                else:
                    self._last_fetched_messages_list = list()
            except ResourceNotExistsError:
                raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process of "
                                f"being created. Failed to get messages list from DynamoDb table.")
            except Exception as e:
                raise Exception(f"Failed to retrieve messages list from DynamoDb table. "
                                f"Exception of type {type(e).__name__} occurred: {str(e)}")
        return self._last_fetched_messages_list

    def get_speechs_list(self, messages_list_id: str) -> list:
        return self.get_fetched_messages_list(messages_list_id=messages_list_id)

    @staticmethod
    def _speech_item_to_dict(speech_item: Speech) -> dict:
        return {"speech": speech_item.speech, "probability": speech_item.probability_value}

    def _speechs_list_object_to_dict(self, speechs_list_object: SpeechsList) -> dict:
        speech_items_list = list()
        for speech_item in speechs_list_object.speechs_list:
            speech_items_list.append(self._speech_item_to_dict(speech_item=speech_item))
        return {"id": speechs_list_object.interaction_type_names_list[0], "speechItems": speech_items_list}

    def post_new_speechs_list(self, speechs_list: SpeechsList):
        if self.is_admin_mode is not True:
            raise Exception(f"In order to post a new speechs list, the admin mode must be activated but was {self.is_admin_mode}")
        else:
            try:
                speechs_list_dict = self._speechs_list_object_to_dict(speechs_list_object=speechs_list)
                print(f"Posting speechs list : {speechs_list_dict}")
                self.dynamodb.put_item(TableName=self.table_name, Item=self.utils.python_to_dynamodb(speechs_list_dict))
            except ResourceNotExistsError:
                raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
            except Exception as e:
                raise Exception(f"Failed to save speechs list to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

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
            self.dynamodb.put_item(TableName=self.table_name, Item=self.utils.python_to_dynamodb(item_dict))
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, user_id: str):
        """ Deletes attributes from table in Dynamodb resource. """
        self.last_user_id = user_id
        try:
            self.dynamodb.delete_item(TableName=self.table_name, Key={self.primary_key_name: user_id})
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to delete attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to delete attributes in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    @property
    def last_messages_list_id(self) -> str:
        return self._last_messages_list_id
    
    @last_messages_list_id.setter
    def last_messages_list_id(self, last_messages_list_id: str) -> None:
        raise_if_variable_not_expected_type(value=last_messages_list_id, expected_type=str, variable_name="last_messages_list_id")
        self._last_messages_list_id = last_messages_list_id


class DynamoDbNotificationsSubscribers(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str, create_table: Optional[bool] = True):
        super().__init__(table_name=table_name, region_name=region_name, primary_key_name="updatesUserId", create_table=create_table)

    def get_user_subscriptions(self, updates_user_id: str):
        try:
            response = self.dynamodb.get_item(TableName=self.table_name,
                Key={"updatesUserId": self.utils.python_to_dynamodb(updates_user_id)}, ConsistentRead=True)

            if "Item" in response:
                item = response["Item"]
                if isinstance(item, dict) and self.primary_key_name in item.keys():
                    item.pop(self.primary_key_name)
                    if len(item) > 0:
                        # If there is an ID field, then that we remove it from the Item dict, and if after that the length of the item values
                        # is superior to 0, we know we have at least one field other than the id, which is the key of a subscription group.
                        return self.utils.dynamodb_to_python(item)
            return None
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process of "
                            f"being created. Failed to get user subscriptions from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve user subscriptions from DynamoDb table. "
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def add_new_subscribed_group_to_user(self, updates_user_id: str, group_key: str):
        try:
            user_subscriptions = self.get_user_subscriptions(updates_user_id=updates_user_id)
            if user_subscriptions is None:
                print(f"Adding the user with the updates_user_id : {updates_user_id} to the subscription group {group_key}")
                self.dynamodb.put_item(TableName=self.table_name, Item=self.utils.python_to_dynamodb({
                    "updatesUserId": updates_user_id,
                    group_key: True
                }))
            else:
                print(f"Adding the subscription group {group_key} to an existing user with the updates_user_id : {updates_user_id}")
                self.dynamodb.update_item(TableName=self.table_name,
                                          Key={self.primary_key_name: self.utils.python_to_dynamodb(updates_user_id)},
                                          UpdateExpression=f"set {group_key} = :value",
                                          ExpressionAttributeValues={":value": self.utils.python_to_dynamodb(True)},
                                          ReturnValues="UPDATED_NEW")
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to add a new subscribed group to an user in DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to add a new subscribed group to an user in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")


if __name__ == "__main__":
    notifs = DynamoDbNotificationsSubscribers(table_name="test_notifications", region_name="eu-west-3")
    # notifs.add_new_subscribed_group_to_user(updates_user_id="test", group_key="blyat")
    print(notifs.get_user_subscriptions(updates_user_id="test"))

    """""
    messages_db = DynamoDbMessagesAdapter(is_admin_mode=True, table_name="test_messages", region_name="eu-west-3")
    INTERACTION_TYPE_QUESTION_DO_YOU_WANT_INFOS_ABOUT_THE_GAME = "question_do-you-want-infos-about-the-game"
    MSGS_DO_YOU_WANT_INFOS_ABOUT_THE_GAME = SpeechsList().types(INTERACTION_TYPE_QUESTION_DO_YOU_WANT_INFOS_ABOUT_THE_GAME).speechs({
        Speech().add_text("Tant pis, le projet de Polemika est cool, tu veut en savoir plus ?").set_prob(1): 1,
    })
    # messages_db.post_new_speechs_list(MSGS_DO_YOU_WANT_INFOS_ABOUT_THE_GAME)
    # print(messages_db.get_messages_of_category(category_id="question_do-you-want-infos-about-the-game").to_dict())
    """""
