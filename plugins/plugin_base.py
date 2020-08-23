from abc import abstractmethod


class PluginBase:
    # Exist to make it easier to detect if a class if a plugin of any class type.
    pass


class PluginCodeGenerationBase(PluginBase):
    @abstractmethod
    def execute(self, **kwargs):
        raise Exception("Execute method of the plugin must be implemented. "
                        "It will be the method that will be run when your plugin will be execute. "
                        "Also, all the classical class methods (like __init__) will be run like usual.")
