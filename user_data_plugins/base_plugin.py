import abc
from typing import List, Dict, Any, Optional

class MissingAttributeKeyException(Exception):
    pass

class UserDataBasePlugin:
    def __init__(self):
        pass

    @abc.abstractmethod
    def register_plugin(self, skill):
        raise NotImplementedError("register_plugin not implemented")

    @abc.abstractmethod
    def register_new_user(self) -> str:
        raise NotImplementedError("register_new_user not implemented")

    @abc.abstractmethod
    def get_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, Any]:
        raise NotImplementedError("get_attributes not implemented")

    def get_attribute(self, user_id: str, attribute_key: str) -> Any:
        returned_values: Dict[str, Any] = self.get_attributes(
            user_id=user_id, attributes_keys=[attribute_key]
        )
        try:
            return returned_values[attribute_key]
        except KeyError as e:
            raise MissingAttributeKeyException(e)

    @abc.abstractmethod
    def set_attributes(self, user_id: str, attributes_items: Dict[str, Any]) -> Dict[str, bool]:
        raise NotImplementedError("set_attributes not implemented")

    def set_attribute(self, user_id: str, attribute_key: str, attribute_value: Any) -> bool:
        returned_successes: Dict[str, bool] = self.set_attributes(
            user_id=user_id, attributes_items={attribute_key: attribute_value}
        )
        try:
            return returned_successes[attribute_key]
        except KeyError as e:
            raise MissingAttributeKeyException(e)

    @abc.abstractmethod
    def delete_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, bool]:
        raise NotImplementedError("delete_attributes not implemented")

    def delete_attribute(self, user_id: str, attribute_key: str) -> bool:
        returned_successes: Dict[str, bool] = self.delete_attributes(
            user_id=user_id, attributes_keys=[attribute_key]
        )
        try:
            return returned_successes[attribute_key]
        except KeyError as e:
            raise MissingAttributeKeyException(e)

    @abc.abstractmethod
    def remove_attributes(self, user_id: str, attributes_keys: List[str]) -> Dict[str, Any]:
        raise NotImplementedError("remove_attributes not implemented")

    def remove_attribute(self, user_id: str, attribute_key: str) -> Any:
        returned_values: Dict[str, Any] = self.remove_attributes(
            user_id=user_id, attributes_keys=[attribute_key]
        )
        try:
            return returned_values[attribute_key]
        except KeyError as e:
            raise MissingAttributeKeyException(e)
