import os
from typing import List

from inoft_vocal_engine.plugins.plugin_base import PluginBase, PluginCodeGenerationBase
from inoft_vocal_engine.skill_settings.skill_settings import Settings


def plugins_load(settings: Settings) -> List[PluginCodeGenerationBase]:
    plugins_dir_path = os.path.dirname(os.path.abspath(__file__))
    cores_instances_of_code_generation_plugins: List[PluginCodeGenerationBase] = list()
    # We separate the different type of plugins in different lists, because different plugins will
    # not be executed at the same time, or need to same arguments in their execute function.

    # The activated plugins variable is a list containing with the dir name of all the activated plugins
    for plugin_dir_name in settings.plugins.activated_plugings:
        current_plugin_dirpath = os.path.join(plugins_dir_path, plugin_dir_name)
        if not os.path.isdir(current_plugin_dirpath):
            raise Exception(f"The plugin named {plugin_dir_name} has not been found at {current_plugin_dirpath}. Did you type the name right ?")
        else:
            current_plugin_core_filepath = os.path.join(current_plugin_dirpath, "core.py")
            if not os.path.isfile(current_plugin_core_filepath):
                raise Exception(f"The plugin named {plugin_dir_name} has been found at {current_plugin_dirpath}.\n"
                                f"But no file named core.py has been found at the root of this folder.\n"
                                f"Maybe try to re-download the plugin, or it is not compatible with your version of the Inoft Vocal Engine.")
            else:
                import importlib
                import importlib.util
                spec = importlib.util.spec_from_file_location("plugin_core", current_plugin_core_filepath)
                current_plugin_core_module = importlib.util.module_from_spec(spec=spec)
                spec.loader.exec_module(current_plugin_core_module)

                vars_current_plugin_core_module = vars(current_plugin_core_module)
                if "Core" not in vars_current_plugin_core_module.keys():
                    raise Exception(f"The class named Core is missing from the plugin core file at {current_plugin_core_filepath}")
                else:
                    current_plugin_core_class_type = vars_current_plugin_core_module["Core"]

                    from inspect import getmro
                    current_plugin_core_class_parents = getmro(current_plugin_core_class_type)
                    if PluginBase not in current_plugin_core_class_parents:
                        raise Exception(f"The Core class of plugin {current_plugin_dirpath} found at {current_plugin_core_filepath} "
                                        f"was not is not using one of the valid type of plugins parent classes. "
                                        f"It had the following classes : {current_plugin_core_class_parents}")
                    else:
                        if PluginCodeGenerationBase in current_plugin_core_class_parents:
                            cores_instances_of_code_generation_plugins.append(current_plugin_core_class_type())
                        else:
                            raise Exception(f"No valid type of Plugin parent class had been found for the Core class found at {current_plugin_core_filepath}")

    print(cores_instances_of_code_generation_plugins)


