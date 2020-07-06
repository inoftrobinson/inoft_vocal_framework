import jinja2

from inoft_vocal_engine.bixby_core.templates.templates_access import TemplatesAccess
from inoft_vocal_engine.safe_dict import SafeDict
from inoft_vocal_engine.utils.general import load_json

model_dict = SafeDict(load_json("F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_engine/bixby_core/test_model.json"))
intents = model_dict.get("intents").to_dict()

class Core:
    def render(self):
        out = TemplatesAccess().endpoints_template.render(intents=intents)
        print(out)

    @staticmethod
    def write_to_file(text: str, filepath: str):
        with open(filepath, "w+") as file:
            file.write(text)

Core().render()
