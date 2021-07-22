from typing import Optional, Any, List, Dict, Type, Tuple
from StructNoSQL import TableDataModel, BaseField, FieldSetter, FieldGetter, FieldRemover, QueryMetadata

from inoft_vocal_framework.middlewares.inoft_vocal_engine.database_clients import InoftVocalEngineCachingTable


class BaseUserTableDataModel(TableDataModel):
    # userId = BaseField(field_type=str, required=True)
    accountProjectTableKeyId = BaseField(field_type=str, required=True)
    thenState = BaseField(field_type=str, required=False)
    lastIntentHandler = BaseField(field_type=str, required=False)

class UserDataClient:
    """
    A wrapper above an InoftVocalEngineCachingTable that :
    - Restrict operations on records (ie, put_record, delete_record)
    - Automatically add the appropriate key_value for each operation call.
    """
    def __init__(
            self, data_model: Type[TableDataModel], table_id: str, region_name: str,
            engine_account_id: str, engine_project_id: str, engine_api_key: str,
            user_id: str,
    ):
        self.user_id = user_id
        self.account_project_table_user_id: str = f"{engine_project_id}::{engine_project_id}::{table_id}::{user_id}"
        self._table = InoftVocalEngineCachingTable(
            data_model=data_model, table_id=table_id, region_name=region_name,
            engine_account_id=engine_account_id, engine_project_id=engine_project_id, engine_api_key=engine_api_key
        )

    def clear_cached_data(self):
        return self._table.clear_cached_data()
    
    def clear_cached_data_for_record(self, record_primary_key: str):
        return self._table.clear_cached_data_for_record(record_primary_key=record_primary_key)
    
    def clear_pending_update_operations(self):
        return self._table.clear_pending_update_operations()
    
    def clear_pending_remove_operations(self):
        return self._table.clear_pending_remove_operations()
    
    def clear_pending_operations(self):
        return self._table.clear_pending_operations()
    
    def clear_cached_data_and_pending_operations(self):
        return self._table.clear_cached_data_and_pending_operations()
    
    def has_pending_update_operations(self) -> bool:
        return self._table.has_pending_update_operations()
    
    def has_pending_remove_operations(self) -> bool:
        return self._table.has_pending_remove_operations()
    
    def has_pending_operations(self) -> bool:
        return self._table.has_pending_operations()
    
    def commit_update_operations(self):
        return self._table.commit_update_operations()
    
    def commit_remove_operations(self):
        return self._table.commit_remove_operations()
    
    def commit_operations(self):
        self._table.clear_cached_data()
        return self._table.commit_operations()

    def query_field(
            self, field_path: str, query_kwargs: Optional[dict] = None,
            pagination_records_limit: Optional[int] = None,
            filter_expression: Optional[Any] = None, data_validation: bool = True, **additional_kwargs
    ) -> Tuple[Optional[dict], QueryMetadata]:
        return self._table.query_field(
            key_value=self.account_project_table_user_id, 
            field_path=field_path, query_kwargs=query_kwargs,
            pagination_records_limit=pagination_records_limit,
            filter_expression=filter_expression,
            data_validation=data_validation, 
            **additional_kwargs
        )

    def query_multiple_fields(
            self, getters: Dict[str, FieldGetter], pagination_records_limit: Optional[int] = None,
            filter_expression: Optional[Any] = None, data_validation: bool = True, **additional_kwargs
    ) -> Tuple[Optional[dict], QueryMetadata]:
        return self._table.query_multiple_fields(
            key_value=self.account_project_table_user_id,
            getters=getters,
            pagination_records_limit=pagination_records_limit,
            filter_expression=filter_expression,
            data_validation=data_validation,
            **additional_kwargs
        )

    def get_field(self, field_path: str, query_kwargs: Optional[dict] = None) -> Optional[Any]:
        return self._table.get_field(key_value=self.account_project_table_user_id, field_path=field_path, query_kwargs=query_kwargs)

    def get_multiple_fields(self, getters: Dict[str, FieldGetter]) -> Optional[dict]:
        return self._table.get_multiple_fields(key_value=self.account_project_table_user_id, getters=getters)

    def update_field(self, field_path: str, value_to_set: Any, query_kwargs: Optional[dict] = None) -> bool:
        return self._table.update_field(
            key_value=self.account_project_table_user_id, 
            field_path=field_path, value_to_set=value_to_set, query_kwargs=query_kwargs
        )
    
    def update_field_return_old(
            self, field_path: str, value_to_set: Any, 
            query_kwargs: Optional[dict] = None, data_validation: bool = True
    ) -> Tuple[bool, Optional[Any]]:
        return self._table.update_field_return_old(
            key_value=self.account_project_table_user_id, 
            field_path=field_path, value_to_set=value_to_set, 
            query_kwargs=query_kwargs, data_validation=data_validation
        )

    def update_multiple_fields(self, setters: List[FieldSetter]) -> bool:
        return self._table.update_multiple_fields(
            key_value=self.account_project_table_user_id, setters=setters
        )
    
    def update_multiple_fields_return_old(
            self, setters: Dict[str, FieldSetter], data_validation: bool = True
    ) -> Tuple[bool, Dict[str, Optional[Any]]]:
        return self._table.update_multiple_fields_return_old(
            key_value=self.account_project_table_user_id,
            setters=setters, data_validation=data_validation
        )

    def remove_field(
            self, field_path: str, query_kwargs: Optional[dict] = None, data_validation: bool = True
    ) -> Optional[Any]:
        return self._table.remove_field(
            key_value=self.account_project_table_user_id, 
            field_path=field_path, query_kwargs=query_kwargs, 
            data_validation=data_validation
        )

    def remove_multiple_fields(
            self, removers: Dict[str, FieldRemover], data_validation: bool = True
    ) -> Dict[str, Optional[Any]]:
        return self._table.remove_multiple_fields(
            key_value=self.account_project_table_user_id, 
            removers=removers, data_validation=data_validation
        )
    
    def delete_field(self, field_path: str, query_kwargs: Optional[dict] = None) -> bool:
        return self._table.delete_field(
            key_value=self.account_project_table_user_id, 
            field_path=field_path, query_kwargs=query_kwargs
        )

    def delete_multiple_fields(self, removers: Dict[str, FieldRemover]) -> Dict[str, bool]:
        return self._table.delete_multiple_fields(
            key_value=self.account_project_table_user_id, removers=removers
        )
    
    def grouped_remove_multiple_fields(
            self, removers: Dict[str, FieldRemover], data_validation: bool = True
    ) -> Optional[Dict[str, Any]]:
        return self._table.grouped_remove_multiple_fields(
            key_value=self.account_project_table_user_id,
            removers=removers, data_validation=data_validation
        )
    
    def grouped_delete_multiple_fields(self, removers: List[FieldRemover]) -> bool:
        return self._table.grouped_delete_multiple_fields(
            key_value=self.account_project_table_user_id,
            removers=removers
        )
