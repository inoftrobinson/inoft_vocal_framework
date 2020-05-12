# -*- coding: utf-8 -*-

import re
from typing import Optional

from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.skill_builder.skill_settings import Settings
from inoft_vocal_framework.session_utils import add_new_played_category  # todo: remove this dependance
from inoft_vocal_framework.general_utils import pick_msg # todo: and remove this dependance too
from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type

# todo: make all functions cross platform ;)
# todo: likely it will be smarter to make a SpeechAlexa object, a SpeechGoogle object, and a SpeechBixby object.

class SpeechsList:
    def __init__(self, id: str, speechs: list = None):
        self.id = id
        self.speechs_list = speechs
        self._use_database_dynamic_messages = None

    @property
    def use_database_dynamic_messages(self):
        if self._use_database_dynamic_messages is None:
            self._use_database_dynamic_messages = Settings().settings.get("use_database_dynamic_messages").to_bool()
        return self._use_database_dynamic_messages

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str) -> None:
        raise_if_variable_not_expected_type(value=id, expected_type=str, variable_name="id")
        self._id = id

    def speechs(self, speechs_list: list):
        self.speechs_list = speechs_list
        return self

    def pick(self, ids_messages_to_exclude=None) -> str:
        if self.use_database_dynamic_messages is True:
            from inoft_vocal_framework.databases.dynamodb.dynamodb import DynamoDbMessagesAdapter
            self.speechs_list = DynamoDbMessagesAdapter(table_name="test_messages", region_name="eu-west-3").get_speechs_list(messages_list_id=self.id)
        return pick_msg(self.speechs_list)

    def do_not_register(self):
        self.should_register_when_picking = True
        return self

    def register_played(self):
        add_new_played_category(handler_input=None, new_played_interactions_types=self.interaction_type_name)
        return self

class Speech:

    VALID_INTERPRET_AS = ('characters', 'spell-out', 'cardinal', 'number',
                          'ordinal', 'digits', 'fraction', 'unit', 'date',
                          'time', 'telephone', 'address', 'interjection', 'expletive')

    VALID_PROSODY_ATTRIBUTES = {
        'rate': ('x-slow', 'slow', 'medium', 'fast', 'x-fast'),
        'pitch': ('x-low', 'low', 'medium', 'high', 'x-high'),
        'volume': ('silent', 'x-soft', 'soft', 'medium', 'loud', 'x-loud')
    }

    VALID_VOICE_NAMES = ('Ivy', 'Joanna', 'Joey', 'Justin', 'Kendra', 'Kimberly',
                        'Matthew', 'Salli', 'Nicole', 'Russell', 'Amy', 'Brian', 'Emma',
                        'Aditi', 'Raveena', 'Hans', 'Marlene', 'Vicki', 'Conchita', 'Enrique',
                        'Carla', 'Giorgio', 'Mizuki', 'Takumi', 'Celine', 'Lea', 'Mathieu')

    VALID_EMPHASIS_LEVELS = ('strong', 'moderate', 'reduced')

    def __init__(self):
        self.probability_value = None
        self.text = ""
        self.speech = ""

    def from_dict(self, speech_safedict: SafeDict):
        self.probability_value = speech_safedict.get("probability").to_float(default=None)
        self.speech = speech_safedict.get("speech").to_str()
        return self

    def set_prob(self, probability_value: float):
        self.probability_value = probability_value
        return self

    def get_text(self) -> str:
        return self.text

    def speak(self) -> str:
        return f'<speak>{self.speech}</speak>'

    def add_text(self, text: str):
        self.text += text
        self.speech += text
        return self

    def say_as(self, text: str, name_interpret_as: str, is_nested: Optional[bool] = False):
        if name_interpret_as not in self.VALID_INTERPRET_AS:
            raise ValueError('The interpret-as provided to say_as is not valid')

        ssml = f'<say-as interpret-as="{name_interpret_as}">{text}</say-as>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def prosody(self, text: str, rate: str = "medium", pitch: str = "medium", volume: str = "medium", is_nested: Optional[bool] = False):
        if rate not in self.VALID_PROSODY_ATTRIBUTES['rate']:
            if re.match(r'^\d+%$', rate) is None:
                raise ValueError('The rate provided to prosody is not valid')

        if pitch not in self.VALID_PROSODY_ATTRIBUTES['pitch']:
            if re.match(r'^(\+|\-)+\d+(\.\d+)*%$', pitch) is None:
                raise ValueError('The pitch provided to prosody is not valid')

        if volume not in self.VALID_PROSODY_ATTRIBUTES['volume']:
            raise ValueError('The volume provided to prosody is not valid')

        ssml = '<prosody rate="{rate}" pitch="{pitch}" volume="{volume}">' \
               '{value}</prosody>'.format(rate=rate, pitch=pitch, volume=volume, value=text)

        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def sub(self, text: str, alias, is_nested: Optional[bool] = False):
        ssml = f'<sub alias="{alias}">{text}</sub>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def lang(self, text: str, lang_key: str, is_nested: Optional[bool] = False):
        ssml = f'<lang xml:lang="{lang_key}">{text}</lang>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def voice(self, text: str, voice_name: str, is_nested: Optional[bool] = False):
        if voice_name not in self.VALID_VOICE_NAMES:
            raise ValueError('The name provided to voice is not valid')

        ssml = f'<voice name="{voice_name}">{text}</voice>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def pause(self, time_ms: int, is_nested: Optional[bool] = False):
        ssml = f"<break time='{time_ms}ms'/>"
        if is_nested:
            return ssml

        self.speech += ssml
        return self

    def whisper(self, text: str, is_nested: Optional[bool] = False):
        ssml = f'<amazon:effect name="whispered">{text}</amazon:effect>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def audio_file(self, src_url: str, is_nested: Optional[bool] = False):
        """
        :param src_url:
        :param is_nested:
        :return:
        """

        ssml = '<audio src="{}" />'.format(src_url)

        if is_nested:
            return ssml

        self.speech += ssml
        return self

    def emphasis(self, text: str, level: str, is_nested: Optional[bool] = False):

        if level not in self.VALID_EMPHASIS_LEVELS:
            raise ValueError('The level provided to emphasis is not valid')

        ssml = '<emphasis level="strong">{}</emphasis>'.format(text)

        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def p(self, text: str, is_nested: Optional[bool] = False):
        ssml = f'<p>{text}</p>'
        if is_nested:
            return ssml

        self.text += text
        self.speech += ssml
        return self

    def escape(self):
        """
        escapes any special characters that will cause SSML to be invalid
        :return:
        """
        pass
