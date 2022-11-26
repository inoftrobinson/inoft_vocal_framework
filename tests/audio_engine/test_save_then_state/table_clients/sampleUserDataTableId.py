from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.database_clients import InoftVocalEngineCachingTable
from inoft_vocal_framework.user_data_plugins.inoft_vocal_engine_structnosql_plugin.table_models import BaseUserTableDataModel

user_data_inoft_vocal_engine_table_client = InoftVocalEngineCachingTable(
    engine_account_id="b1fe5939-032b-462d-92e0-a942cd445096",
    engine_project_id="4ede8b70-46f6-4ae2-b09c-05a549194c8e",
    engine_api_key="a2bf5ff8-bbd3-4d01-b695-04138ee19b42",
    region_name='eu-west-3', table_id='sampleUserDataTableId',
    data_model=BaseUserTableDataModel
)
