import os
import time
from typing import List

from inoft_vocal_engine.audacity.client import AudacityClient
from inoft_vocal_engine.speech_synthesis.polly.client import PollyClient
from inoft_vocal_engine.speech_synthesis.polly import VOICES
from inoft_vocal_engine.inoft_vocal_markup.deserializer import Deserializer, DialogueLine
from inoft_vocal_engine import Sound
from inoft_vocal_engine.speech_synthesis.polly.voice_object import Voice


class TextToAudacity:
    def __init__(self, character_names_to_voices: dict):
        self._audacity = None
        self._polly = None
        self.character_names_to_voices = character_names_to_voices
        self.available_character_names = list(character_names_to_voices.keys())
        self.dialogue_deserializer = Deserializer(characters_names=self.available_character_names)

    @property
    def audacity(self) -> AudacityClient:
        if self._audacity is None:
            self._audacity = AudacityClient()
        return self._audacity

    @property
    def polly(self) -> PollyClient:
        if self._polly is None:
            self._polly = PollyClient()
        return self._polly

    def synthesize_text_to_project(self, text: str):
        dialogues_lines = self.dialogue_deserializer.deserialize(text=text)
        return self.synthesize_dialogues_lines_to_project(dialogues_lines=dialogues_lines)

    def synthesize_dialogues_lines_to_project(self, dialogues_lines: List[DialogueLine], dirpath_to_save_to: str):
        synthesized_dialogues: List[Sound] = list()

        element_lines_dirpath = os.path.join(dirpath_to_save_to, "lines")
        if not os.path.isdir(element_lines_dirpath):
            os.makedirs(element_lines_dirpath)

        for i_dialogue, dialogue in enumerate(dialogues_lines):
            if dialogue.character_name not in self.available_character_names:
                if "default" not in self.available_character_names:
                    raise Exception(f"The character name {dialogue.character_name} has not been found in the available character"
                                    f" names : {self.available_character_names} and no character named default has been found .")
                else:
                    dialogue.character_name = "default"

            voice_for_current_dialogue: Voice = self.character_names_to_voices[dialogue.character_name]
            if not isinstance(voice_for_current_dialogue, Voice):
                raise Exception(f"The voice object for the character name {dialogue.character_name} was "
                                f"not of type Voice but was of type : {type(voice_for_current_dialogue)}")

            from text_unidecode import unidecode
            character_name_without_accents = unidecode(dialogue.character_name)
            current_dialogue_line_filename = f"line_{str(i_dialogue).zfill(3)}__{character_name_without_accents}_{voice_for_current_dialogue.id}.mp3"

            filepath_to_save_to = os.path.join(element_lines_dirpath, current_dialogue_line_filename)
            if os.path.exists(filepath_to_save_to):
                current_synthesized_dialogue = Sound(filepath_to_save_to)
                synthesized_dialogues.append(current_synthesized_dialogue)
                print(f"Find and will be using existing file at {filepath_to_save_to}")
            else:
                synthesized_dialogue_filepath = self.polly.synthesize(text=dialogue.line_content,
                    voice_id=voice_for_current_dialogue.id, filepath_to_save_to=filepath_to_save_to)
                print(f"Synthesized new audio file to {filepath_to_save_to}")

                if synthesized_dialogue_filepath is not None:
                    current_synthesized_dialogue = Sound(synthesized_dialogue_filepath)
                    synthesized_dialogues.append(current_synthesized_dialogue)

        if len(synthesized_dialogues) > 0:
            self.audacity.delete_all_tracks()
            project_seconds_duration = 0.0

            for i_audio_dialogue, audio_dialogue in enumerate(synthesized_dialogues):
                self.audacity.import_file(audio_dialogue.local_filepath, track_number=i_audio_dialogue)

                if i_audio_dialogue > 0:
                    self.audacity.set_clip(clip_id=i_audio_dialogue, track_number=0, seconds_start=project_seconds_duration)
                project_seconds_duration += audio_dialogue.duration_seconds

            # self.audacity.mix_and_render_tracks()



if __name__ == "__main__":
    client = TextToAudacity(character_names_to_voices={
        "Léo": VOICES.French_France_Male_MATHIEU,
        "Willie": VOICES.French_France_Female_CELINE,
        "Menu": VOICES.Icelandic_Iceland_Male_KARL
    })

    text_ = """
    *Léo* Je voudrais tuer tous les allemands !\n
    *Willie* Comment on fait ? Il faudrait qu'ils croient qu'on est dans leur camp ?\n
    *Léo* Je ne sais pas exactement, on trouvera. Ont pourrait essayer de capturer un Boche ou deux.\n
    *Willie* Oui, ils sont très très très très moches les allemands, il faut tousse les tuer...
    """

    client.synthesize_text_to_project(text=text_)
    input()

    """
    leo = Sound(polly.synthesize(text="Ont pourrais essayer de récuperer des informations en utilisant leurs radio.",
                           voice_id=VOICES.French_France_Male_MATHIEU.id,
                                 filepath_to_save_to="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_engine/speech_synthesis/polly/leo.mp3"))

    willie = Sound(polly.synthesize(text="Comment ont ferrais, il faudrais qu'ils croient qu'ont soit dans leurs camp ?",
                                    voice_id=VOICES.French_France_Female_CELINE.id,
                                    filepath_to_save_to="F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_engine/speech_synthesis/polly/willie.mp3"))
    """

    leo = Sound("F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_engine/speech_synthesis/polly/leo.mp3")
    willie = Sound("F:/Inoft/skill_histoire_decryptage_1/inoft_vocal_engine/speech_synthesis/polly/willie.mp3")

    audacity.delete_all_tracks()
    audacity.import_file(leo.local_filepath, track_number=1)
    # audacity.import_file(willie.local_filepath, track_number=2)
    audacity.set_clip(clip_id=1, track_number=0, seconds_start=leo.duration_seconds)
