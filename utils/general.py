from typing import Optional


def get_dict_of_all_custom_defined_variables_of_class(class_object: object) -> dict:
    # From https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
    output_vars_dict = dict()
    vars_of_object = vars(class_object)
    for key_var, value_var in vars_of_object.items():
        if not callable(getattr(class_object, key_var)) and not key_var.startswith("__"):
            output_vars_dict[key_var] = value_var
    return output_vars_dict

def is_text_ssml(text_or_ssml: str) -> bool:
    return "<speak>" in text_or_ssml and "</speak>" in text_or_ssml

def generate_uuid4() -> str:
    from uuid import uuid4 as uuid4_generator
    id_str = str(uuid4_generator())
    print(f"Generated id : {id_str}")
    return id_str

def load_yaml(filepath: str, encoding: Optional[str] = "utf-8") -> dict or list:
    from yaml import safe_load, YAMLError
    with open(filepath, "r", encoding=encoding) as file_stream:
        try:
            return safe_load(file_stream)
        except YAMLError as error:
            raise Exception(f"The yaml file was not valid, and caused an error when loading."
                            f"Please check the file or recreate it with the cli : {error}")

def load_json(filepath: str, encoding: Optional[str] = "utf-8") -> dict or list:
    from json import load as json_load
    with open(filepath, "r", encoding=encoding) as file_stream:
        try:
            return json_load(file_stream)
        except Exception as error:
            raise Exception(f"The json file was not valid, and caused an error when loading."
                            f"Please check the file or recreate it with the cli : {error}")

def get_all_files_in_dir(dirpath: str) -> list:
    from os import listdir
    from os.path import isfile, join
    return [filepath for filepath in listdir(dirpath) if isfile(join(dirpath, filepath))]

def get_all_dirs_in_dir(dirpath: str) -> list:
    from os import listdir
    from os.path import isdir, join
    return [filepath for filepath in listdir(dirpath) if isdir(join(dirpath, filepath))]
