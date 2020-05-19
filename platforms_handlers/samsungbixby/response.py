class Response:
    json_key: str

    def __init__(self):
        self._text = str()

    def say(self, text_or_ssml: str):
        self.text = text_or_ssml

    def reprompt(self, text_or_ssml: str):
        print("Reprompt of bixby not yet implemented")

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        if not isinstance(text, str):
            raise Exception(f"text was type {type(text)} which is not valid value for his parameter.")
        self._text = text

    def to_dict(self):
        return {
            "text": self.text
        }

