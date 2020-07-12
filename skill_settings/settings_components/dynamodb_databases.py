from typing import Optional


class DynamoDBTable:
    def __init__(self, db_table_name: str, db_region_name: str):
        self.db_table_name = db_table_name
        self.db_region_name = db_region_name

class DatabaseSessionsUsersData(DynamoDBTable):
    def __init__(self, db_table_name: str = None, db_region_name: str = None, disable_database: Optional[bool] = False):
        super().__init__(db_table_name=db_table_name, db_region_name=db_region_name)
        self.disable_database = disable_database
        if self.disable_database is not True:
            if self.db_table_name is None:
                pass
                # prompt_database_warning_message(variable_name="db_table_name", instance_type=DatabaseSessionsUsersData)
            if self.db_region_name is None:
                pass
                # prompt_database_warning_message(variable_name="db_region_name", instance_type=DatabaseSessionsUsersData)


class DatabaseMessagesContent(DynamoDBTable):
    def __init__(self, db_table_name: str = None, db_region_name: str = None, disable_database: Optional[bool] = False):
        super().__init__(db_table_name=db_table_name, db_region_name=db_region_name)
        self.disable_database = disable_database

class DatabaseUsersNotificationsSubscriptions(DynamoDBTable):
    def __init__(self, db_table_name: str = None, db_region_name: str = None, disable_database: Optional[bool] = False):
        super().__init__(db_table_name=db_table_name, db_region_name=db_region_name)
        self.disable_database = disable_database
