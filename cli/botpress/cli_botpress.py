import os
from typing import List

import click
from inoft_vocal_framework.cli.cli_cache import CliCache
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.general import get_all_files_in_dir, get_all_dirs_in_dir
from inoft_vocal_framework.cli.botpress.content_element_object import ContentElement


class BotpressCore:
    def __init__(self):
        self.selected_bot_dirname = None
        self.selected_bot_dirpath = None

    def handle(self):
        def prompt_user_to_select_botpress_dirpath():
            return click.prompt(text="What is the installation folderpath of your Botpress ?\n"
                                     "For example C:/Program Files (x86)/botpress-v12_8_1-win-x64")

        botpress_dirpath = CliCache.cache().get("botpress_dirpath").to_str(default=None)
        if botpress_dirpath is None:
            botpress_dirpath = prompt_user_to_select_botpress_dirpath()

        while not os.path.exists(botpress_dirpath):
            click.echo(f"The folderpath : {botpress_dirpath} was not found.")
            botpress_dirpath = prompt_user_to_select_botpress_dirpath()

        filenames_in_botpress_folder = get_all_files_in_dir(botpress_dirpath)
        while "bp.exe" not in filenames_in_botpress_folder:
            filenames_in_botpress_folder = get_all_files_in_dir(botpress_dirpath)
            click.echo(f"The folder you specified has your botpress folder ({botpress_dirpath} is valid.\n"
                       f"Yet the bp.exe file has not been found in your Botpress folder."
                       f"You must have not select the right folder, or you have an issue with Botpress and need to re-install it.")
            botpress_dirpath = prompt_user_to_select_botpress_dirpath()

        CliCache().cache().put("botpress_dirpath", botpress_dirpath)
        CliCache().save_cache_to_yaml()

        botpress_bots_dirpath = os.path.join(botpress_dirpath, "data", "bots")
        if not os.path.exists(botpress_bots_dirpath):
            raise Exception(f"No data/bots folder has been found in your Botpress directory. Did you already created at least one Bot ?\n"
                            f"The Inoft Vocal Engine has check at the following path : {botpress_bots_dirpath}")
        else:
            bots_dirnames = get_all_dirs_in_dir(botpress_bots_dirpath)
            if len(bots_dirnames) > 0:
                click.echo("Which Bot would like to select ?")
                for bot_folder in bots_dirnames:
                    click.echo(f"{bot_folder} - 1")

                while True:
                    bot_number = str(click.prompt(f"Please type a number between 1 and {len(bots_dirnames)}"))
                    if bot_number.isdigit():
                        bot_index = int(bot_number) - 1
                        self.selected_bot_dirname = bots_dirnames[bot_index]
                        self.selected_bot_dirpath = os.path.join(botpress_bots_dirpath, self.selected_bot_dirname)
                        break

        self._content_elements_to_audacity(content_elements=self._text_elements_to_content_elements())

    def _text_elements_to_content_elements(self) -> List[ContentElement]:
        builtin_text_filepath = os.path.join(self.selected_bot_dirpath, "content-elements", "builtin_text.json")
        if not os.path.isfile(builtin_text_filepath):
            raise Exception(f"No file has been found at {builtin_text_filepath}")
        else:
            from inoft_vocal_framework.utils.general import load_json
            list_all_text_elements = load_json(builtin_text_filepath)

            from inoft_vocal_framework.inoft_vocal_markup.deserializer import Deserializer
            inoft_vocal_markup_deserializer = Deserializer(characters_names=["Léo", "Willie", "Menu"])

            content_elements: List[ContentElement] = list()
            for text_element in list_all_text_elements:
                current_content_element = ContentElement()

                text_element_safedict = SafeDict(text_element)
                text_content = text_element_safedict.get("formData").get("text$fr").to_str(default=None)
                if text_content is not None:
                    current_content_element.dialogues_lines = inoft_vocal_markup_deserializer.deserialize(text=text_content)
                    # todo: give the ability to select the language to deserialize

                current_content_element.created_by = text_element_safedict.get("createdBy").to_str(default=None)
                current_content_element.created_on = text_element_safedict.get("createdOn").to_str(default=None)
                current_content_element.modified_on = text_element_safedict.get("modifiedOn").to_str(default=None)
                content_elements.append(current_content_element)

            return content_elements

    def _content_elements_to_audacity(self, content_elements: List[ContentElement]):
        from inoft_vocal_framework.audacity.text_to_audacity import TextToAudacity
        from inoft_vocal_framework.speech_synthesis.polly import VOICES
        client = TextToAudacity(character_names_to_voices={
            "Léo": VOICES.French_France_Male_MATHIEU,
            "Willie": VOICES.French_France_Female_CELINE,
            "Luc": VOICES.Russian_Russia_Male_MAXIM,
            "Menu": VOICES.Icelandic_Iceland_Male_KARL,
            "default": VOICES.French_France_Female_LEA
        })

        for content_element in content_elements[200:]:
            if isinstance(content_element.dialogues_lines, list) and len(content_element.dialogues_lines) > 0:
                client.synthesize_dialogues_lines_to_project(dialogues_lines=content_element.dialogues_lines)
                print("done")
                input()



if __name__ == "__main__":
    BotpressCore().handle()
