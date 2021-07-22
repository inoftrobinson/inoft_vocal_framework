from typing import Type
from StructNoSQL import ExternalDynamoDBApiCachingTable, TableDataModel, PrimaryIndex, ExternalDynamoDBApiBasicTable


class InoftVocalEngineBasicTable(ExternalDynamoDBApiBasicTable):
    def __init__(
            self, data_model: Type[TableDataModel], table_id: str, region_name: str,
            engine_account_id: str, engine_project_id: str, engine_api_key: str,
    ):
        self.engine_account_id = engine_account_id
        self.engine_project_id = engine_project_id
        super().__init__(
            api_http_endpoint=f'http://127.0.0.1:5000/api/v1/{self.engine_account_id}/{self.engine_project_id}/database-client?accessToken={engine_api_key}',
            primary_index=PrimaryIndex(hash_key_name='accountProjectTableKeyId', hash_key_variable_python_type=str),
            data_model=data_model, base_payload={'tableId': table_id}
        )

class InoftVocalEngineCachingTable(ExternalDynamoDBApiCachingTable):
    def __init__(
            self, data_model: Type[TableDataModel], table_id: str, region_name: str,
            engine_account_id: str, engine_project_id: str, engine_api_key: str,
    ):
        self.engine_account_id = engine_account_id
        self.engine_project_id = engine_project_id
        super().__init__(
            api_http_endpoint=f'http://127.0.0.1:5000/api/v1/{self.engine_account_id}/{self.engine_project_id}/database-client?accessToken={engine_api_key}',
            primary_index=PrimaryIndex(hash_key_name='accountProjectTableKeyId', hash_key_variable_python_type=str),
            data_model=data_model, base_payload={'tableId': table_id}
        )
