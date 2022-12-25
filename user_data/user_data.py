from typing import Any, List, Dict
from inoft_vocal_framework.user_data_plugins.base_plugin import UserDataBasePlugin


class UserDataClient:
    def __init__(self, user_data_plugin: UserDataBasePlugin, user_id: str):
        self.user_data_plugin = user_data_plugin
        self.user_id = user_id

    def get_attributes(self, attributes_keys: List[str]) -> Dict[str, Any]:
        return self.user_data_plugin.get_attributes(user_id=self.user_id, attributes_keys=attributes_keys)

    def get_attribute(self, attribute_key: str) -> Any:
        return self.user_data_plugin.get_attribute(user_id=self.user_id, attribute_key=attribute_key)

    def set_attributes(self, attributes_items: Dict[str, Any]) -> Dict[str, bool]:
        return self.user_data_plugin.set_attributes(user_id=self.user_id, attributes_items=attributes_items)

    def set_attribute(self, attribute_key: str, attribute_value: Any) -> bool:
        return self.user_data_plugin.set_attribute(user_id=self.user_id, attribute_key=attribute_key, attribute_value=attribute_value)

    def delete_attributes(self, attributes_keys: List[str]) -> Dict[str, bool]:
        return self.user_data_plugin.delete_attributes(user_id=self.user_id, attributes_keys=attributes_keys)

    def delete_attribute(self, attribute_key: str) -> bool:
        return self.user_data_plugin.delete_attribute(user_id=self.user_id, attribute_key=attribute_key)

    def remove_attributes(self, attributes_keys: List[str]) -> Dict[str, Any]:
        return self.user_data_plugin.remove_attributes(user_id=self.user_id, attributes_keys=attributes_keys)

    def remove_attribute(self, attribute_key: str) -> Any:
        return self.user_data_plugin.remove_attribute(user_id=self.user_id, attribute_key=attribute_key)
