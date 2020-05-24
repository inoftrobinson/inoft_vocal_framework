class Voice:
    def __init__(self, gender: str, id: str, language_code: str, language_name: str, name: str, supported_engines: list or str):
        self.id = id
        self.gender = gender
        self.name = name
        self.language_code = language_code
        self.language_name = language_name
        self.supported_engines = supported_engines
