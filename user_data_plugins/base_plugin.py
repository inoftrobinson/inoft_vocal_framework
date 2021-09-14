import abc
from typing import List, Dict, Any


class UserDataBasePlugin:
    def __init__(self):
        pass

    @abc.abstractmethod
    def register_plugin(self, skill):
        raise Exception("register_plugin not implemented")

    @abc.abstractmethod
    def register_new_user(self) -> str:
        raise Exception("register_new_user not implemented")

    @abc.abstractmethod
    def get_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, Any]:
        raise Exception("get_attributes not implemented")

    @abc.abstractmethod
    def set_attributes(self, user_id: str, attributes_items: Dict[str, Any]) -> Dict[str, bool]:
        raise Exception("set_attributes not implemented")

    @abc.abstractmethod
    def delete_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, bool]:
        raise Exception("delete_attributes not implemented")
