def get_dict_of_all_custom_defined_variables_of_class(class_object: object) -> dict:
    # From https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    output_vars_dict = dict()
    vars_of_object = vars(class_object)
    for key_var, value_var in vars_of_object.items():
        if not callable(getattr(class_object, key_var)) and not key_var.startswith("__"):
            output_vars_dict[key_var] = value_var
    return output_vars_dict

def is_text_ssml(text_or_ssml: str):
    is_ssml = False
    if "<speak>" in text_or_ssml:
        # For ssml, the speak balise must start the string, so if we find other chars than
        # whitespaces before the balise, we consider that the string to not be a ssml string.
        before_start_balise, after_start_balise = text_or_ssml.split("<speak>", maxsplit=1)
        are_all_chars_in_before_start_balise_whitespaces = True
        for char in before_start_balise:
            if char != " ":
                are_all_chars_in_before_start_balise_whitespaces = False
        if are_all_chars_in_before_start_balise_whitespaces is True:
            is_ssml = True
    return is_ssml

def generate_uuid4() -> str:
    from uuid import uuid4 as uuid4_generator
    id_str = str(uuid4_generator())
    print(f"Generated id : {id_str}")
    return id_str
