from typing import Union, List, Optional, Dict, Any
from uuid import uuid4

from StructNoSQL import FieldGetter, FieldSetter, FieldRemover

from inoft_vocal_framework import InoftSkill
from inoft_vocal_framework.user_data_plugins.base_plugin import UserDataBasePlugin
from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.database_clients import \
    InoftVocalEngineCachingTable, InoftVocalEngineBasicTable


class UserDataInoftVocalEngineStructNoSQLPlugin(UserDataBasePlugin):
    def __init__(self, table_client: Union[InoftVocalEngineBasicTable, InoftVocalEngineCachingTable]):
        super().__init__()
        self.table_client = table_client

    def register_plugin(self, skill: InoftSkill):
        if isinstance(self.table_client, InoftVocalEngineCachingTable):
            skill.on_interaction_end.append(lambda: self.table_client.commit_operations())

    def make_account_project_table_key(self, key_value) -> str:
        return f"{self.table_client.engine_account_id}::{self.table_client.engine_project_id}::{self.table_client.engine_table_id}::{key_value}"

    def register_new_user(self) -> str:
        for i in range(10):
            generated_user_id: str = str(uuid4())
            account_project_table_user_id: str = self.make_account_project_table_key(key_value=generated_user_id)
            existing_account_project_table_key_id: Optional[str] = self.table_client.get_field(
                key_value=account_project_table_user_id, field_path='accountProjectTableKeyId'
            )
            if existing_account_project_table_key_id is None:
                put_record_success: bool = self.table_client.put_record(
                    record_dict_data={'accountProjectTableKeyId': account_project_table_user_id}
                )
                return generated_user_id
        raise Exception("Could not create an unique user-id after 10 attempts")

    def get_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, Any]:
        retrieved_fields: Optional[Dict[str, Any]] = self.table_client.get_multiple_fields(
            key_value=user_id, getters={key: FieldGetter(field_path=key) for key in attributes_keys}
        )
        return retrieved_fields if retrieved_fields is not None else {key: None for key in attributes_keys}

    def set_attributes(self, user_id: str, attributes_items: Dict[str, Any]) -> Dict[str, bool]:
        update_success: bool = self.table_client.update_multiple_fields(
            key_value=user_id, setters=[FieldSetter(field_path=key, value_to_set=value) for key, value in attributes_items.items()]
        )
        return {key: update_success for key in attributes_items.keys()}

    def delete_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, bool]:
        deletion_successes: Dict[str, bool] = self.table_client.delete_multiple_fields(
            key_value=user_id, removers={key: FieldRemover(field_path=key) for key in attributes_keys}
        )
        return deletion_successes
