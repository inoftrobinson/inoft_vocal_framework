from inoft_vocal_framework.safe_dict import SafeDict
from json import loads as json_loads


class NestedObjectToDict:
    @staticmethod
    def _remove_start_underscores_from_string_key(string_key: str) -> str:
        index_first_underscore = None
        if string_key is not None:
            for i_char in range(len(string_key)):
                if string_key[i_char] == "_":
                    if index_first_underscore is None:
                        index_first_underscore = i_char
                else:
                    if index_first_underscore is not None:
                        cleaned_string_key = string_key[:index_first_underscore] + string_key[i_char:]
                        return cleaned_string_key
                    else:
                        return string_key
        return string_key

    @staticmethod
    def _is_object_empty(class_object) -> bool:
        functions_of_object = dir(class_object)
        # We use dir and not vars, because vars do not include the functions of the class

        if "do_not_include" in functions_of_object:
            # We make sure that the do_not_include var is a function that can be called and not a shadow variable
            if class_object.do_not_include():
                return True
        return False

    @staticmethod
    def _apply_return_transformations(class_object) -> bool:
        """
        :param class_object:
        :return: bool True if the object contained the return_transformations method and it has been applied, else bool False
        """
        functions_of_object = dir(class_object)
        # We use dir and not vars, because vars do not include the functions of the class

        if "return_transformations" in functions_of_object:
            # We make sure that the return_transformations var is a function that can be called and not a shadow variable
            class_object.return_transformations()
            return True
        return False

    @staticmethod
    def _process_potential_nested_object(class_object, key_names_identifier_objects_to_go_into: list, is_first_parent_object=False) -> dict:
        for accepted_parent_key_name in key_names_identifier_objects_to_go_into:
            if hasattr(class_object, accepted_parent_key_name):
                is_class_object_empty = NestedObjectToDict._is_object_empty(class_object=class_object)

                if not is_class_object_empty:
                    NestedObjectToDict._apply_return_transformations(class_object=class_object)
                    # We only need to apply the return transformations here, since an object that could
                    # contain some return transformations will always be passed to this recurrent function.
                    # If we called the return transformations somewhere else, we could end up calling them multiple times.

                    output_dict = dict()
                    keys_to_pop_after_loop_finished = list()

                    main_vars_dict = vars(class_object)
                    if isinstance(main_vars_dict, dict):
                        for main_var_key, main_var_object in main_vars_dict.items():
                            found_accepted_key_name_in_vars_of_current_object = False

                            if isinstance(main_var_object, list):
                                for i in range(len(main_var_object)):
                                    found_accepted_key_name_in_vars_of_current_child_item_object = False

                                    for accepted_child_key_name in key_names_identifier_objects_to_go_into:
                                        if hasattr(main_var_object[i], accepted_child_key_name):
                                            # If the object has an accepted child key name, we will set the values
                                            # of the object inside of a dict with the child key name as the key dict
                                            found_accepted_key_name_in_vars_of_current_child_item_object = True

                                            nested_object_accepted_key_value = getattr(main_var_object[i].__class__, accepted_child_key_name)
                                            cleaned_key = NestedObjectToDict._remove_start_underscores_from_string_key(nested_object_accepted_key_value)

                                            item_output_dict = NestedObjectToDict._process_potential_nested_object(class_object=main_var_object[i],
                                                key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

                                            main_var_object[i] = {cleaned_key: item_output_dict} if cleaned_key is not None else item_output_dict
                                            # If the key is None, it means that the object needed to be go into to process it, but should not be
                                            # put inside a dict with its the cleaned_key has its name. This is the case for list items, for
                                            # examples for items of a carousel, they will be objects, that should be put in a list of items of
                                            # the carousel, and have their values put right away in a dict, and not inside a dict called "item"
                                            # that will contain all the values of the item.

                                    if found_accepted_key_name_in_vars_of_current_child_item_object is False:
                                        # Otherwise, we just process the value and put it back in the list, without creating a dict
                                        main_var_object[i] = NestedObjectToDict._process_potential_nested_object(class_object=main_var_object[i],
                                            key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)
                            else:
                                for accepted_child_key_name in key_names_identifier_objects_to_go_into:
                                    if hasattr(main_var_object, accepted_child_key_name):
                                        found_accepted_key_name_in_vars_of_current_object = True

                                        is_main_var_object_empty = NestedObjectToDict._is_object_empty(class_object=main_var_object)
                                        # We remove an object that is defined as empty (see the called function for details)
                                        if is_main_var_object_empty:
                                            keys_to_pop_after_loop_finished.append(main_var_key)
                                        else:
                                            nested_object_accepted_key_value = getattr(main_var_object.__class__, accepted_child_key_name)
                                            cleaned_key = NestedObjectToDict._remove_start_underscores_from_string_key(nested_object_accepted_key_value)

                                            output_dict[cleaned_key] = NestedObjectToDict._process_potential_nested_object(class_object=main_var_object,
                                               key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

                                        # The loop we are currently in is just to see if the object has the attribute that tell use that it is an object
                                        # to go deeper into. If we found at least one, we do not need to look at the same object a second time.
                                        break

                            if found_accepted_key_name_in_vars_of_current_object is False and main_var_object is not None:
                                do_not_include_current_item = False

                                if isinstance(main_var_object, str):
                                    if main_var_object.replace(" ", "") == "":
                                        do_not_include_current_item = True

                                elif isinstance(main_var_object, dict) or isinstance(main_var_object, list):
                                    if not len(main_var_object) > 0:
                                        do_not_include_current_item = True
                                    else:
                                        if isinstance(main_var_object, dict):
                                            for key_item_main_var_object, value_item_main_var_object in main_var_object.items():
                                                main_var_object[key_item_main_var_object] = NestedObjectToDict._process_potential_nested_object(
                                                    class_object=value_item_main_var_object, key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)
                                        elif isinstance(main_var_object, list):
                                            for i_item_main_var_object, item_main_var_object in enumerate(main_var_object):
                                                main_var_object[i_item_main_var_object] = NestedObjectToDict._process_potential_nested_object(
                                                    class_object=item_main_var_object, key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

                                if not do_not_include_current_item:
                                    cleaned_key = NestedObjectToDict._remove_start_underscores_from_string_key(main_var_key)
                                    output_dict[cleaned_key] = main_var_object

                    for key_to_pop in keys_to_pop_after_loop_finished:
                        # We pop the keys after the loop has finished, to avoid
                        # issues while modifying the dict items during the loop.
                        main_vars_dict.pop(key_to_pop)

                    if not is_first_parent_object:
                        return output_dict
                    else:
                        parent_object_accepted_key_value = getattr(class_object.__class__, accepted_parent_key_name)
                        cleaned_parent_key = NestedObjectToDict._remove_start_underscores_from_string_key(parent_object_accepted_key_value)
                        return {cleaned_parent_key: output_dict}

        # If no accepted_parent_key_name has been found, we return the object not
        # modified (to handle when we pass list or dict items trough the function.
        return class_object

    @staticmethod
    def get_dict_from_nested_object(object_to_process, key_names_identifier_objects_to_go_into: list) -> dict:
        if isinstance(key_names_identifier_objects_to_go_into, str):
            key_names_identifier_objects_to_go_into = [key_names_identifier_objects_to_go_into]

        output_dict = NestedObjectToDict._process_potential_nested_object(class_object=object_to_process,
           key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into, is_first_parent_object=True)
        if not isinstance(output_dict, dict):
            raise Exception(f"The following nested object converted to a dict was not of type dict but of type {type(output_dict)}")

        print(output_dict)
        return output_dict

    @staticmethod
    def _process_and_set_dict_to_object(object_class_to_set_to, dict_object: dict, key_names_identifier_objects_to_go_into: list):
        unprocessed_vars_dict = vars(object_class_to_set_to)
        from types import MappingProxyType
        if isinstance(unprocessed_vars_dict, MappingProxyType):
            # Sometimes the vars dict is put in a MappingProxy object instead of a dict. A MappingProxy is like a dict,
            # but cannot have its values modified, so we convert it back to a dict since we will need to modify the values.
            unprocessed_vars_dict = dict(unprocessed_vars_dict)

        vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names = SafeDict()
        for key_unprocessed_var in unprocessed_vars_dict.keys():
            processed_current_key_name = NestedObjectToDict.get_json_key_from_variable_name(variable_name=key_unprocessed_var)
            vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names.put(dict_key=processed_current_key_name,
                                                                                              value_to_put=key_unprocessed_var)

        keys_to_pop_after_loop_finished = list()
        for key_request_element, value_request_element in dict_object.items():
            key_request_element = str(key_request_element).replace(" ", "")
            # In the received requests, there can sometimes be spaces in a key before closing it with an apostrophe.
            # Having a single empty space at the end of a key would not be the same as the key without the space.

            current_unprocessed_variable_name = vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names.get(key_request_element).to_any()
            if current_unprocessed_variable_name is not None:
                current_child_element_object = unprocessed_vars_dict[current_unprocessed_variable_name]

                if current_child_element_object is not None:
                    found_accepted_key_name_in_vars_of_current_object = False

                    if isinstance(value_request_element, dict) or isinstance(value_request_element, list):
                        for accepted_child_key_name in key_names_identifier_objects_to_go_into:
                            if hasattr(current_child_element_object, accepted_child_key_name):
                                found_accepted_key_name_in_vars_of_current_object = True

                                NestedObjectToDict.process_and_set_json_request_to_object(
                                    object_class_to_set_to=unprocessed_vars_dict[current_unprocessed_variable_name],
                                    request_json_dict_stringed_dict_or_list=value_request_element,
                                    key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

                    if not found_accepted_key_name_in_vars_of_current_object:
                        do_not_include_current_item = False

                        if (isinstance(value_request_element, str)
                        or (type(value_request_element) == type and "str" in value_request_element.__bases__)):
                            if value_request_element.replace(" ", "") == "":
                                do_not_include_current_item = True

                        elif (isinstance(value_request_element, dict) or isinstance(value_request_element, list)
                        or (type(value_request_element) == type and ("dict" in value_request_element.__bases__
                                                                     or "list" in value_request_element.__bases__))):
                            if not len(value_request_element) > 0:
                                do_not_include_current_item = True

                        if not do_not_include_current_item:
                            # if (type(value_request_element) == type(current_child_element_object)
                            # or (((isinstance(value_request_element, float) or isinstance(value_request_element, int))
                            #     and type(current_child_element_object) in [int, float]))):
                            # For some variables, we might receive them in int or float, where the framework would store
                            # them with the other variable type. So we say that if the received variable is an int or a float,
                            # its considered compatible with the variable in the object if it is also a float or an int.

                            custom_set_from_function = getattr(current_child_element_object, "custom_set_from", None)
                            if custom_set_from_function is None:
                                unprocessed_vars_dict[current_unprocessed_variable_name] = value_request_element
                            # elif type(value_request_element) in current_child_element_object.__bases__:
                            else:
                                custom_set_from_function(value_request_element)

        for key_to_pop in keys_to_pop_after_loop_finished:
            unprocessed_vars_dict.pop(key_to_pop)

    @staticmethod
    def _process_and_set_list_to_object(object_class_to_set_to, list_object: list, key_names_identifier_objects_to_go_into: list):
        unprocessed_vars_dict = vars(object_class_to_set_to)
        from types import MappingProxyType
        if isinstance(unprocessed_vars_dict, MappingProxyType):
            # Sometimes the vars dict is put in a MappingProxy object instead of a dict. A MappingProxy is like a dict,
            # but cannot have its values modified, so we convert it back to a dict since we will need to modify the values.
            unprocessed_vars_dict = dict(unprocessed_vars_dict)

        vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names = SafeDict()
        for key_unprocessed_var in unprocessed_vars_dict.keys():
            processed_current_key_name = NestedObjectToDict.get_json_key_from_variable_name(variable_name=key_unprocessed_var)
            vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names.put(dict_key=processed_current_key_name,
                                                                                              value_to_put=key_unprocessed_var)

        for child_item in list_object:
            if isinstance(child_item, dict):
                for key_child_item, value_child_item in child_item.items():
                    current_unprocessed_variable_name = vars_safedict_key_processed_keys_names_with_value_unprocessed_variables_names.get(key_child_item).to_any()
                    if current_unprocessed_variable_name is not None:
                        current_child_element_object = unprocessed_vars_dict[current_unprocessed_variable_name]

                        if current_child_element_object is not None:
                            found_accepted_key_name_in_vars_of_current_object = False

                            for accepted_child_key_name in key_names_identifier_objects_to_go_into:
                                if hasattr(current_child_element_object, accepted_child_key_name):
                                    found_accepted_key_name_in_vars_of_current_object = True

                                    NestedObjectToDict.process_and_set_json_request_to_object(
                                        object_class_to_set_to=unprocessed_vars_dict[current_unprocessed_variable_name],
                                        request_json_dict_stringed_dict_or_list=value_child_item,
                                        key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

                            if not found_accepted_key_name_in_vars_of_current_object:
                                do_not_include_current_item = False

                                if (isinstance(value_child_item, str)
                                or (type(value_child_item) == type and "str" in value_child_item.__bases__)):
                                    if value_child_item.replace(" ", "") == "":
                                        do_not_include_current_item = True

                                elif (isinstance(value_child_item, dict) or isinstance(value_child_item, list)
                                or (type(value_child_item) == type and ("dict" in value_child_item.__bases__
                                                                        or "list" in value_child_item.__bases__))):
                                    if not len(value_child_item) > 0:
                                        do_not_include_current_item = True

                                if not do_not_include_current_item:
                                    custom_set_from_function = getattr(current_child_element_object, "custom_set_from", None)
                                    if custom_set_from_function is None:
                                        unprocessed_vars_dict[current_unprocessed_variable_name] = value_child_item
                                    else:
                                        custom_set_from_function(value_child_item)

            elif isinstance(child_item, list) or (type(child_item) == type and "list" in child_item.__bases__):
                NestedObjectToDict._process_and_set_list_to_object(object_class_to_set_to=child_item, list_object=child_item,
                                                                   key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)

    @staticmethod
    def process_and_set_json_request_to_object(object_class_to_set_to, request_json_dict_stringed_dict_or_list, key_names_identifier_objects_to_go_into: list):
        if isinstance(request_json_dict_stringed_dict_or_list, dict):
            NestedObjectToDict._process_and_set_dict_to_object(object_class_to_set_to=object_class_to_set_to,
                                                               dict_object=request_json_dict_stringed_dict_or_list,
                                                               key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)
        elif isinstance(request_json_dict_stringed_dict_or_list, str):
            NestedObjectToDict._process_and_set_dict_to_object(object_class_to_set_to=object_class_to_set_to,
                key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into,
                dict_object=NestedObjectToDict.get_dict_from_json(stringed_json_dict=request_json_dict_stringed_dict_or_list))
        elif isinstance(request_json_dict_stringed_dict_or_list, list):
            NestedObjectToDict._process_and_set_list_to_object(object_class_to_set_to=object_class_to_set_to,
                                                               list_object=request_json_dict_stringed_dict_or_list,
                                                               key_names_identifier_objects_to_go_into=key_names_identifier_objects_to_go_into)
        else:
            raise Exception(f"The request_json_dict_stringed_dict_or_list variable is of type "
                            f"{type(request_json_dict_stringed_dict_or_list)} but must of type {dict}, {str} or {list}")

    @staticmethod
    def get_dict_from_json(stringed_json_dict: str) -> dict:
        try:
            return json_loads(stringed_json_dict)
        except Exception as e:
            print(f"Warning ! The following string has tried to be converted in the get_dict_from_json function"
                  f"of the nested_object_to_dict file, but the following error occurred, returning None : {e}")
            return None

    @staticmethod
    def get_json_key_from_variable_name(variable_name: str):
        return NestedObjectToDict._remove_start_underscores_from_string_key(variable_name)


