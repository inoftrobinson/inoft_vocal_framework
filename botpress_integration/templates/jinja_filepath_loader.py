from jinja2 import BaseLoader, TemplateNotFound
from os.path import exists, getmtime

class JinjaFilepathLoader(BaseLoader):
    def __init__(self, filepath):
        self.filepath = filepath

    def get_source(self, environment, template):
        if not exists(self.filepath):
            raise TemplateNotFound(template)
        mtime = getmtime(self.filepath)
        with open(self.filepath) as f:
            source = f.read()
        return source, self.filepath, lambda: mtime == getmtime(self.filepath)
