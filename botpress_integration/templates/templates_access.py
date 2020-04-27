from jinja2 import Template, FileSystemLoader, Environment


class TemplatesAccess:
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader, lstrip_blocks=True, trim_blocks=True)

    _skill_app_template = None
    _launch_request_handler_template = None
    _intent_name_condition_template = None
    _state_handler_template = None
    _message_logic_template = None
    _set_variable_logic_template = None
    _handler_logic_template = None
    _messages_template = None

    @staticmethod
    def _get_template(template_name: str) -> Template:
        return TemplatesAccess.env.get_template(template_name)

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
    def message_logic_template(self) -> Template:
        if TemplatesAccess._message_logic_template is None:
            TemplatesAccess._message_logic_template = TemplatesAccess._get_template("message_logic.tem")
        return TemplatesAccess._message_logic_template

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
