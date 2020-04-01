class SafeDict:
    def __init__(self, classic_dict=None, overloaded_navigated_dict=None):
        if classic_dict is None:
            classic_dict = dict()
        if isinstance(classic_dict, list):
            output_dict = dict()
            for i in range(len(classic_dict)):
                output_dict[i] = classic_dict[i]
            classic_dict = output_dict
        elif not isinstance(classic_dict, dict):
            try:
                classic_dict = dict(classic_dict)
            except Exception:
                try:
                    classic_dict = dict(vars(classic_dict))
                except Exception:
                    print(f"The following variable could not be converted to a dict in order to create a SafeDict object : {classic_dict}")

        if isinstance(classic_dict, dict):
            self.classic_dict = classic_dict
            if not isinstance(overloaded_navigated_dict, dict):
                self.navigated_dict = self.classic_dict
            else:
                self.navigated_dict = overloaded_navigated_dict
        else:
            self.classic_dict = dict()
            if not isinstance(overloaded_navigated_dict, dict):
                self.navigated_dict = dict()
            else:
                self.navigated_dict = overloaded_navigated_dict

    
    def reset_navigated_dict(self):
        self.navigated_dict = self.classic_dict

    def retrieve_navigated_dict_object(self, reset_navigated_dict=True):
        if isinstance(self.navigated_dict, dict) or isinstance(self.navigated_dict, list):
            # A dict or a list will not make a copy of the value, but
            # point a reference to the object, so we need to copy them.
            navigated_dict_object = self.navigated_dict.copy()
        else:
            navigated_dict_object = self.navigated_dict

        if reset_navigated_dict is True:
            self.reset_navigated_dict()
        return navigated_dict_object

    def retrieve_navigated_dict_values(self, reset_navigated_dict=True):
        if isinstance(self.navigated_dict, dict):
            navigated_dict_values = list(self.navigated_dict.values())

            if len(navigated_dict_values) > 1:
                navigated_dict_values = navigated_dict_values
            elif len(navigated_dict_values) > 0:
                navigated_dict_values = navigated_dict_values[0]
            else:
                navigated_dict_values = None

            if reset_navigated_dict is True:
                self.reset_navigated_dict()
            return navigated_dict_values
        else:
            navigated_dict_values = self.navigated_dict
            self.reset_navigated_dict()
            return navigated_dict_values

    def get(self, dict_key: str):
        if isinstance(self.navigated_dict, dict) and dict_key in self.navigated_dict.keys():
            self.navigated_dict = self.navigated_dict[dict_key]
        else:
            self.navigated_dict = None
        return self

    def get_set(self, dict_key: str, value_to_set_if_missing={}):
        if isinstance(self.navigated_dict, dict):
            if dict_key not in self.navigated_dict.keys():
                self.navigated_dict[dict_key] = value_to_set_if_missing

            self.navigated_dict = self.navigated_dict[dict_key]
        return self

    def put(self, dict_key, value_to_put):
        if isinstance(self.navigated_dict, dict) and dict_key is not None:
            if value_to_put is None:
                value_to_put = ""
            self.navigated_dict[dict_key] = value_to_put
        else:
            print(f"Warning ! Tried to put a value into a dict of a SafeDict, but the current navigated dict was not pointing to a dict object !")
        return self

    def pop(self, dict_key: str):
        if isinstance(self.navigated_dict, dict) and isinstance(dict_key, str) and dict_key in self.navigated_dict.keys():
            self.navigated_dict.pop(dict_key)
        else:
            print(f"Warning ! Tried to pop a key of a dict of a SafeDict, but the current navigated dict was not pointing to a dict object !")
        return self

    def process_any_safedicts_in_dict_or_list_to_dict(self, dict_or_list_to_process):
        if isinstance(dict_or_list_to_process, list):
            for i in range(len(dict_or_list_to_process)):
                dict_or_list_to_process[i] = self.process_any_safedicts_in_dict_or_list_to_dict(dict_or_list_to_process[i])
        elif isinstance(dict_or_list_to_process, dict):
            for key in dict_or_list_to_process.keys():
                dict_or_list_to_process[key] = self.process_any_safedicts_in_dict_or_list_to_dict(dict_or_list_to_process[key])
        elif isinstance(dict_or_list_to_process, SafeDict):
            return dict_or_list_to_process.to_dict()
        else:
            return dict_or_list_to_process

    def to_str(self, default="", reset_navigated_dict=True) -> str:
        navigated_dict_values = self.retrieve_navigated_dict_values(reset_navigated_dict=reset_navigated_dict)
        if isinstance(navigated_dict_values, str):
            return navigated_dict_values
        else:
            return default

    def to_bool(self, default=False, reset_navigated_dict=True) -> bool:
        navigated_dict_values = self.retrieve_navigated_dict_values(reset_navigated_dict=reset_navigated_dict)
        if isinstance(navigated_dict_values, bool):
            return navigated_dict_values
        else:
            return default

    def to_int(self, default=0, reset_navigated_dict=True) -> int:
        navigated_dict_values = self.retrieve_navigated_dict_values(reset_navigated_dict=reset_navigated_dict)
        try:
            int_value = int(navigated_dict_values)
            return int_value
        except Exception as cannot_convert_error:
            return default
        
    def to_float(self, default=0.0, reset_navigated_dict=True) -> float:
        navigated_dict_values = self.retrieve_navigated_dict_values(reset_navigated_dict=reset_navigated_dict)
        try:
            float_value = float(navigated_dict_values)
            return float_value
        except Exception as cannot_convert_error:
            return default

    def to_list(self, default=[], reset_navigated_dict=True) -> list:
        navigated_dict_values = self.retrieve_navigated_dict_values(reset_navigated_dict=reset_navigated_dict)
        navigated_dict_values = self.process_any_safedicts_in_dict_or_list_to_dict(dict_or_list_to_process=navigated_dict_values)
        if isinstance(navigated_dict_values, list):
            return navigated_dict_values
        elif isinstance(navigated_dict_values, dict):
            return list(navigated_dict_values.values())
        else:
            return default

    def to_dict(self, default={}, reset_navigated_dict=True) -> dict:
        navigated_dict_object = self.retrieve_navigated_dict_object(reset_navigated_dict=reset_navigated_dict)
        navigated_dict_object = self.process_any_safedicts_in_dict_or_list_to_dict(dict_or_list_to_process=navigated_dict_object)
        if isinstance(navigated_dict_object, dict):
            return navigated_dict_object
        elif isinstance(navigated_dict_object, list):
            output_dict = dict()
            for i in range(len(navigated_dict_object)):
                output_dict[i] = navigated_dict_object[i]
            return output_dict
        else:
            return default

    def to_safedict(self, default=None, reset_navigated_dict=True):
        navigated_dict_object = self.retrieve_navigated_dict_object(reset_navigated_dict=reset_navigated_dict)
        if navigated_dict_object is not None:
            return SafeDict(navigated_dict_object)
        else:
            return default if default is not None else SafeDict()

    def to_any(self, default=None, reset_navigated_dict=True):
        navigated_dict_object = self.retrieve_navigated_dict_object(reset_navigated_dict=reset_navigated_dict)
        return navigated_dict_object

    def to_specific_type(self, type_to_return: type, reset_navigated_dict=True):
        if type_to_return == str:
            return self.to_str(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == bool:
            return self.to_bool(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == int:
            return self.to_int(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == float:
            return self.to_float(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == list:
            return self.to_list(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == dict:
            return self.to_dict(reset_navigated_dict=reset_navigated_dict)
        elif type_to_return == SafeDict:
            return self.to_safedict(reset_navigated_dict=reset_navigated_dict)
        else:
            raise Exception(f"The following type is not supported by the SafeDict object : {type_to_return}."
                            f"If you post a request in the issues section of the GitHub,"
                            f"i will add the object type that you need to the SafeDict class - Robinson")

    def keys(self):
        return self.navigated_dict.keys()

    def copy(self, reset_navigated_dict=True):
        new_safeDict_copy = SafeDict(classic_dict=self.classic_dict, overloaded_navigated_dict=self.navigated_dict)
        if reset_navigated_dict:
            self.reset_navigated_dict()
        return new_safeDict_copy
