import os
from typing import Tuple, Optional, Any

from cerberus import Validator
from inoft_vocal_framework.safe_dict import SafeDict


def get_settings_safedict() -> SafeDict:
    if Settings.settings_loaded is not True:
        raise Exception(f"The settings have not yet been loaded and are : {Settings.settings_safedict}")
    return Settings.settings_safedict

class Settings:
    settings_safedict = None
    settings_loaded = False

    class ExtendedValidator(Validator):
        def _validate_check_database_field_present(self, check_database_field_present: bool, field: str, value):
            """ {'type': 'boolean'} """
            if check_database_field_present is True and value not in self.document.keys():
                self._error(field, f"The key {value} was missing from the following section : {self.document}")

        def _validate_is_database_not_disabled(self, is_database_not_disabled: bool, field: str, value):
            """ {'type': 'boolean'} """
            if is_database_not_disabled is True and "disable_database" in self.document.keys() and self.document["disable_database"]:
                self._error(field, f"The database is disabled in the following section : {self.document}")

    @property
    def _settings_file_validator_schema(self) -> dict:
        return {
            "default_session_data_timeout": {
                "required": True,
                "type": "integer"
            },
            "sessions_users_data": {
                "required": True,
                "type": "dict",
                "schema": {
                    "disable_database": {
                        "required": False,
                        "type": "boolean",
                    },
                    "database_client": {
                        "required": True,
                        "type": "string",
                        "allowed": ["dynamodb"],
                        "is_database_not_disabled": True,
                        "check_database_field_present": True,
                    },
                    "dynamodb": {
                        "type": "dict",
                        "schema": {
                            "table_name": {
                                "required": True,
                                "type": "string"
                            },
                            "region_name": {
                                "required": True,
                                "type": "string"
                            }
                        }
                    }
                }
            },
            "messages": {
                "required": True,
                "type": "dict",
                "schema": {
                    "use_database_dynamic_messages": {
                        "required": True,
                        "type": "boolean"
                    },
                    "database_client": {
                        "type": "string",
                        "allowed": ["dynamodb"],
                        "required": True,
                        "check_database_field_present": True,
                        "dependencies": {"use_database_dynamic_messages": True}
                    },
                    "dynamodb": {
                        "type": "dict",
                        "schema": {
                            "table_name": {
                                "required": True,
                                "type": "string"
                            },
                            "region_name": {
                                "required": True,
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }

    @property
    def _static_settings_safedict(self):
        return Settings.settings_safedict

    @_static_settings_safedict.setter
    def _static_settings_safedict(self, settings_dict: dict):
        validator = self.ExtendedValidator()
        is_valid = validator.validate(settings_dict, self._settings_file_validator_schema)
        if is_valid is not True:
            raise Exception(f"The settings file was not valid. Please modify it or recreate it : {validator.errors}")
        else:
            Settings.settings_safedict = SafeDict(settings_dict)
            Settings.settings_loaded = True


    def load_yaml(self, settings_filepath: str):
        from inoft_vocal_framework.utils.general import load_yaml
        self._static_settings_safedict = SafeDict(load_yaml(filepath=settings_filepath))

    def load_json(self, settings_filepath: str):
        from inoft_vocal_framework.utils.general import load_json
        self._static_settings_safedict = SafeDict(load_json(filepath=settings_filepath))

