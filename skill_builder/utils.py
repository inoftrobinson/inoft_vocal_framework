def get_function_or_class_from_file_and_path(file_filepath: str, path_qualname: str):
    from os.path import isfile

    if not isfile(file_filepath):
        print(f"SERIOUS WARNING ! The module file containing a callback function at filepath  {file_filepath} "
              f"has not been found. The callback cannot be used. If your interaction that use the callback is not "
              f"working, it is because you have issues with the location of your file containing the callback.")
    else:
        import importlib
        import importlib.util
        module_spec = importlib.util.spec_from_file_location("fileContainingFunctionOrClass", file_filepath)
        if module_spec is not None:
            module_file = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module_file)

            path_list = path_qualname.split(".")
            if len(path_list) > 0:
                vars_module_file = vars(module_file)
                if path_list[0] in vars_module_file:
                    if len(path_list) == 1:
                        # If the path list is only of length one, and that the first element is
                        # found in the vars of the module, we can return it right away.
                        return vars_module_file[path_list[0]]
                    else:
                        # Otherwise we will start a recursive function to handle potentially nested classes or functions.
                        from inspect import getmembers

                        def get_nested_class_or_function(current_nested_class_or_function, path_remaining_elements: list):
                            if len(path_remaining_elements) > 0:
                                class_or_function_name = path_remaining_elements[0]
                                if class_or_function_name == "<locals>":
                                    raise Exception(
                                        f"A callback function cannot be a nested function of another function ({class_or_function_name}) "
                                        "Please make it available from the root of the file or from a class then relaunch the event "
                                        "that inserted the function path of the callback function (redo the entire interaction up to"
                                        "the point where you set the callback to an event).")

                                members_nested_class_or_function = getmembers(current_nested_class_or_function)
                                for tuple_member in members_nested_class_or_function:
                                    if tuple_member[0] == class_or_function_name:
                                        if len(path_remaining_elements) > 1:
                                            return get_nested_class_or_function(current_nested_class_or_function=tuple_member[1],
                                                path_remaining_elements=path_remaining_elements[1:])
                                        else:
                                            return tuple_member[1]
                            return None

                        return get_nested_class_or_function(current_nested_class_or_function=vars_module_file[path_list[0]],
                                                            path_remaining_elements=path_list[1:])
    return None
