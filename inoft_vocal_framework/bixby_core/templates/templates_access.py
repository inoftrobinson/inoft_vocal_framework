from jinja2 import Template, FileSystemLoader, Environment


class TemplatesAccess:
    file_loader = FileSystemLoader("templates")
    env = Environment(loader=file_loader)

    _endpoints_template = None

    @staticmethod
    def _get_template(template_name: str) -> Template:
        return TemplatesAccess.env.get_template(template_name)

    @property
    def endpoints_template(self) -> Template:
        if TemplatesAccess._endpoints_template is None:
            TemplatesAccess._endpoints_template = TemplatesAccess._get_template("endpoints.tem")
        return TemplatesAccess._endpoints_template
