import time

from boto3.session import ResourceNotExistsError

from inoft_vocal_framework.databases.dynamodb.dynamodb_core import DynamoDbCoreAdapter
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.speechs.ssml_builder_core import Speech, SpeechCategory


class DynamoDbAttributesAdapter(DynamoDbCoreAdapter):
    def __init__(self, table_name: str, region_name: str, primary_key_name="id", create_table=True,
                 persistent_attributes_key_name="persistent_attributes", smart_session_attributes_key_name="smart_session_attributes"):
        super().__init__(table_name, region_name)

        self.persistent_attributes_key_name = persistent_attributes_key_name
        self.smart_session_attributes_key_name = smart_session_attributes_key_name

        self._fetchedData = None
        self._last_user_id = None

    # todo: create an option of bandwith optimization by loading the
    #  persistent attributes in the session attributes at the start of the session

    def _fetch_attributes(self, user_id: str) -> SafeDict:
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={"id": user_id}, ConsistentRead=True)
            if "Item" in response:
                from inoft_vocal_framework.databases.dynamodb.dynamodb_utils import dynamodb_to_dict
                return SafeDict(dynamodb_to_dict(response["Item"]))
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
            table = self._get_db_table()
            from inoft_vocal_framework.databases.dynamodb.dynamodb_utils import dict_to_dynamodb
            out = dict_to_dynamodb(item_dict)
            table.put_item(Item=dict_to_dynamodb(item_dict))
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, user_id: str):
        """ Deletes attributes from table in Dynamodb resource. """
        self.last_user_id = user_id
        try:
            table = self._get_db_table()
            table.delete_item(Key={self.primary_key_name: user_id})
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
    def __init__(self, table_name: str, region_name: str, is_admin_mode=False):
        super().__init__(table_name=table_name, region_name=region_name)
        self.is_admin_mode = is_admin_mode
        self._fetched_messages_of_last_category = None
        self._last_category_id = None

    def _speech_dicts_to_speech_items(self, speech_dicts: list) -> list:
        output_list = list()
        for speech_dict in speech_dicts:
            output_list.append(Speech().from_dict(speech_safedict=SafeDict(speech_dict)))
        return output_list

    def _fetch_messages_of_category(self, category_id: str) -> list:
        try:
            table = self.dynamodb.Table(self.table_name)
            response = table.get_item(Key={"id": category_id}, ConsistentRead=True)
            if "Item" in response and "speechItems" in response["Item"]:
                from inoft_vocal_framework.databases.dynamodb.dynamodb_utils import dynamodb_to_dict
                return self._speech_dicts_to_speech_items(dynamodb_to_dict(response["Item"]["speechItems"]))
            else:
                return list()
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} do not exist or in the process of "
                            f"being created. Failed to get messages of category from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to retrieve messages of category from DynamoDb table. "
                            f"Exception of type {type(e).__name__} occurred: {str(e)}")

    def get_messages_of_category(self, category_id: str) -> list:
        if self._fetched_messages_of_last_category is None or category_id != self.last_category_id:
            self._fetched_messages_of_last_category = self._fetch_messages_of_category(category_id=category_id)
        return self._fetched_messages_of_last_category

    def get_speech_category(self, category_id: str) -> SpeechCategory:
        return SpeechCategory().speechs(self.get_messages_of_category(category_id=category_id))

    @staticmethod
    def _speech_item_to_dict(speech_item: Speech) -> dict:
        return {"speech": speech_item.speech, "probability": speech_item.probability_value}

    def _speech_category_object_to_dict(self, speech_category_object: SpeechCategory) -> dict:
        speech_items_list = list()
        for speech_item in speech_category_object.speechs_objects:
            speech_items_list.append(self._speech_item_to_dict(speech_item=speech_item))
        return {"id": speech_category_object.interaction_type_names_list[0], "speechItems": speech_items_list}

    def post_new_category(self, speech_category: SpeechCategory):
        if self.is_admin_mode is not True:
            raise Exception(f"In order to post a new speech category, the admin mode must be activated but was {self.is_admin_mode}")
        else:
            try:
                speech_category_dict = self._speech_category_object_to_dict(speech_category_object=speech_category)
                print(f"Posting category : {speech_category_dict}")
                table = self._get_db_table()
                from inoft_vocal_framework.databases.dynamodb.dynamodb_utils import dict_to_dynamodb
                table.put_item(Item=dict_to_dynamodb(speech_category_dict))
            except ResourceNotExistsError:
                raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
            except Exception as e:
                raise Exception(f"Failed to save speech category to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")


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
            from inoft_vocal_framework.databases.dynamodb.dynamodb_utils import dict_to_dynamodb
            out = dict_to_dynamodb(item_dict)
            table.put_item(Item=dict_to_dynamodb(item_dict))
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to save attributes to DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to save attributes to DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    def delete_attributes(self, user_id: str):
        """ Deletes attributes from table in Dynamodb resource. """
        self.last_user_id = user_id
        try:
            table = self._get_db_table()
            table.delete_item(Key={self.primary_key_name: user_id})
        except ResourceNotExistsError:
            raise Exception(f"DynamoDb table {self.table_name} doesn't exist. Failed to delete attributes from DynamoDb table.")
        except Exception as e:
            raise Exception(f"Failed to delete attributes in DynamoDb table. Exception of type {type(e).__name__} occurred: {str(e)}")

    @property
    def last_category_id(self) -> str:
        return self._last_category_id

    @last_category_id.setter
    def last_category_id(self, last_category_id: str) -> None:
        if not isinstance(last_category_id, str):
            raise Exception(f"last_category_id was type {type(last_category_id)} which is not valid value for his parameter.")
        self._last_category_id = last_category_id

messages_db = DynamoDbMessagesAdapter(is_admin_mode=True, table_name="test_messages", region_name="eu-west-3")

INTERACTION_TYPE_QUESTION_DO_YOU_WANT_INFOS_ABOUT_THE_GAME = "question_do-you-want-infos-about-the-game"
MSGS_DO_YOU_WANT_INFOS_ABOUT_THE_GAME = SpeechCategory().types(INTERACTION_TYPE_QUESTION_DO_YOU_WANT_INFOS_ABOUT_THE_GAME).speechs({
    Speech().add_text("Tant pis, le projet de Polemika est cool, tu veut en savoir plus ?").set_prob(1): 1,
})
# messages_db.post_new_category(MSGS_DO_YOU_WANT_INFOS_ABOUT_THE_GAME)
# print(messages_db.get_messages_of_category(category_id="question_do-you-want-infos-about-the-game").to_dict())
