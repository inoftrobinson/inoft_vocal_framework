from inoft_vocal_framework.safe_dict import SafeDict


class PersistentAttrHelpers:
    default_persistent_attr = dict()
    persistent_attr_safeDict = SafeDict()

    @staticmethod
    def define_default_persistent_attr(default_persistent_attr_dict: dict) -> None:
        PersistentAttrHelpers.default_persistent_attr = default_persistent_attr_dict

    @staticmethod
    def instantiate_attrs(handler_input: SafeDict) -> None:
        attributes = (handler_input.get_set(dict_key="session", value_to_set_if_missing={})
                      .get_set(dict_key="attributes", value_to_set_if_missing={}))

        attributes_dict_keys = attributes.to_dict(reset_navigated_dict=False).keys()

        for default_persistent_attr_key in PersistentAttrHelpers.default_persistent_attr.keys():
            # We use the keys function and not the values, because if the value of a key of the default persistent attr is of
            # None value, it will create an exception with the values function, where as we can access the None value by its key.
            if default_persistent_attr_key not in attributes_dict_keys:
                # Even if the persistent attributes are not null, we still check that every key is present, because a new default persistent attributes
                # might be added, and a user could already have a field containing its persistent attributes that do not contains all the keys.
                print(f"default_persistent_attr_key = {default_persistent_attr_key}")
                attributes.put(dict_key=default_persistent_attr_key, value_to_put=PersistentAttrHelpers.default_persistent_attr[default_persistent_attr_key])

        PersistentAttrHelpers.persistent_attr_safeDict = attributes.copy()

    @staticmethod
    def get_attr(attr_key: str, expected_object_type=None):
        PersistentAttrHelpers.persistent_attr_safeDict.get(attr_key).to_specific_type(type_to_return=expected_object_type)

