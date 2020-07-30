from jinja2 import Template, FileSystemLoader, Environment


class TemplatesAccess:
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    # remove the staticness

    _skill_app_template = None
    _launch_request_handler_template = None
    _intent_name_condition_template = None
    _state_handler_template = None
    _say_action_template = None
    _set_variable_logic_template = None
    _handler_logic_template = None
    _messages_template = None

    @staticmethod
    def _get_template(template_name: str) -> Template:
        return TemplatesAccess.env.get_template(template_name)

    @staticmethod
    def _load_template(template_filepath: str) -> Template:
        from inoft_vocal_engine.inoft_vocal_framework.botpress_integration import JinjaFilepathLoader
        env = Environment(loader=JinjaFilepathLoader(filepath=template_filepath))
        # The JinjaFilepathLoader do not care about the template name, only the full template_filepath.
        return env.get_template(name=None)

    @property
    def skill_app_template(self) -> Template:
        if TemplatesAccess._skill_app_template is None:
            TemplatesAccess._skill_app_template = TemplatesAccess._get_template("skill_app.tem")
        return TemplatesAccess._skill_app_template

    @property
    def launch_request_handler_template(self) -> Template:
        if TemplatesAccess._launch_request_handler_template is None:
            TemplatesAccess._launch_request_handler_template = TemplatesAccess._get_template("launch_request_handler.tem")
        return TemplatesAccess._launch_request_handler_template

    @property
    def intent_name_condition_template(self) -> Template:
        if TemplatesAccess._intent_name_condition_template is None:
            TemplatesAccess._intent_name_condition_template = TemplatesAccess._get_template("intent_name_condition.tem")
        return TemplatesAccess._intent_name_condition_template

    @property
    def state_handler_template(self) -> Template:
        if TemplatesAccess._state_handler_template is None:
            TemplatesAccess._state_handler_template = TemplatesAccess._get_template("state_handler.tem")
        return TemplatesAccess._state_handler_template

    @property
    def say_action_template(self) -> Template:
        if TemplatesAccess._say_action_template is None:
            TemplatesAccess._say_action_template = TemplatesAccess._get_template("say_action.tem")
        return TemplatesAccess._say_action_template

    @say_action_template.setter
    def say_action_template(self, filepath: str):
        TemplatesAccess._say_action_template = self._load_template(template_filepath=filepath)

    @property
    def set_variable_logic_template(self) -> Template:
        if TemplatesAccess._set_variable_logic_template is None:
            TemplatesAccess._set_variable_logic_template = TemplatesAccess._get_template("set_variable_logic.tem")
        return TemplatesAccess._set_variable_logic_template

    @property
    def handler_logic_template(self) -> Template:
        if TemplatesAccess._handler_logic_template is None:
            TemplatesAccess._handler_logic_template = TemplatesAccess._get_template("handler_logic.tem")
        return TemplatesAccess._handler_logic_template

    @property
    def messages_template(self) -> Template:
        if TemplatesAccess._messages_template is None:
            TemplatesAccess._messages_template = TemplatesAccess._get_template("messages.tem")
        return TemplatesAccess._messages_template

    @messages_template.setter
    def messages_template(self, filepath: str):
        TemplatesAccess._messages_template = self._load_template(template_filepath=filepath)

