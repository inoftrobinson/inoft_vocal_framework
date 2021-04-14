from typing import Optional, Any, List, Dict
from StructNoSQL import CachingTable, PrimaryIndex, FieldSetter, FieldGetter, FieldRemover, TableDataModel, BaseField


class BaseDataModel(TableDataModel):
    userId = BaseField(name='userId', field_type=str, required=True)
    thenState = BaseField(name='thenState', field_type=str, required=False)
    lastIntentHandler = BaseField(name='lastIntentHandler', field_type=str, required=False)

class UserDataTableClient(CachingTable):
    def __init__(self, table_name: str, region_name: str):
        primary_index = PrimaryIndex(hash_key_name='userId', hash_key_variable_python_type=str)
        super().__init__(
            table_name=table_name, region_name=region_name,
            data_model=BaseDataModel(),
            primary_index=primary_index,
            auto_create_table=False
            # We set auto_create_table to False, because in a deployment on the inoft-vocal-engine,
            # the application will not have the required permissions to create a table. Its better to
            # get a simple Error from StructNoSQL if the table is missing, than a ClientError from AWS.
        )

class UserData:
    def __init__(self, user_id: str):
        self.table = UserDataTableClient(table_name="user_data_sandbox", region_name="eu-west-3")
        # todo: do not run the try to create table
        self.user_id = user_id
        self._cached_data = dict()

    def get_field(self, field_path: str, query_kwargs: Optional[dict] = None):
        return self.table.get_field(key_value=self.user_id, field_path=field_path, query_kwargs=query_kwargs)

    def get_multiple_fields(self, getters: Dict[str, FieldGetter]):
        return self.table.get_multiple_fields(key_value=self.user_id, getters=getters)

    def update_field(self, field_path: str, value_to_set: Any, query_kwargs: Optional[dict] = None):
        return self.table.update_field(key_value=self.user_id, field_path=field_path, value_to_set=value_to_set, query_kwargs=query_kwargs)

    def update_multiple_fields(self, setters: List[FieldSetter] = None):
        return self.table.update_multiple_fields(key_value=self.user_id, setters=setters)

    def delete_field(self, field_path: str, query_kwargs: Optional[dict] = None):
        return self.table.delete_field(key_value=self.user_id, field_path=field_path, query_kwargs=query_kwargs)

    def delete_multiple_fields(self, removers: Dict[str, FieldRemover]):
        return self.table.delete_multiple_fields(key_value=self.user_id, removers=removers)

    def remove_field(self, field_path: str, query_kwargs: Optional[dict] = None):
        return self.table.remove_field(key_value=self.user_id, field_path=field_path, query_kwargs=query_kwargs)

    def remove_multiple_fields(self, removers: Dict[str, FieldRemover]):
        return self.table.remove_multiple_fields(key_value=self.user_id, removers=removers)

    def put_record(self, record_data_dict: dict):
        return self.table.put_record(record_dict_data=record_data_dict)

    def delete_record(self, indexes_keys_selectors: dict):
        return self.table.delete_record(indexes_keys_selectors=indexes_keys_selectors)