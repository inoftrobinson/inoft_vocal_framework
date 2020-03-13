def raise_invalid_variable_type(variable_value, expected_type, variable_name: str = None):
    raise Exception(f"Invalid type. Received {variable_value} of type {type(variable_value)}" +
                    f"for the {variable_name} variable," if variable_name is None else "" +
                    f" but was expecting a variable of type {type(expected_type)}.")

def raise_if_variable_not_expected_type(value, expected_type, variable_name: str = None):
    if not isinstance(value, expected_type):
        raise_invalid_variable_type(variable_value=value, expected_type=expected_type, variable_name=variable_name)

