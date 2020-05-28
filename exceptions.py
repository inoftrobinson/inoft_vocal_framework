def raise_invalid_variable_type(variable_value, expected_type, variable_name: str = None):
    raise Exception(f"Invalid type. Received {variable_value} of type {type(variable_value)} for the {variable_name} variable,"
                    if variable_name is None else f"but was expecting a variable of type {expected_type}.")

def raise_if_variable_not_expected_type(value, expected_type, variable_name: str = None):
    if not isinstance(value, expected_type):
        raise_invalid_variable_type(variable_value=value, expected_type=expected_type, variable_name=variable_name)

def raise_if_variable_not_expected_type_and_not_none(value, expected_type, variable_name: str = None):
    if value is not None:
        raise_if_variable_not_expected_type(value=value, expected_type=expected_type, variable_name=variable_name)

def raise_if_value_not_in_list(value, list_object: list, variable_name: str = None):
    if not isinstance(list_object, list):
        raise Exception(f"The list object {list_object} must be of type list but was {type(list_object)}")
    if value not in list_object:
        raise Exception(f"The {'variable with value of ' if variable_name is not None else 'value'} {value} "
                        f"was not present in the following list {list_object}")

