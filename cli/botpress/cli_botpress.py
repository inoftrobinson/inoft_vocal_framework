import os
from typing import List

import click

from inoft_vocal_framework.cli.aws_core import AwsCore
from inoft_vocal_framework.cli.cli_cache import CliCache
from inoft_vocal_framework.safe_dict import SafeDict
from inoft_vocal_framework.utils.general import get_all_files_in_dir, get_all_dirs_in_dir
from inoft_vocal_framework.cli.botpress.content_element_object import ContentElement


class BotpressCore(AwsCore):
    def __init__(self):
        super().__init__(clients_to_load=[AwsCore.CLIENT_BOTO_SESSION, AwsCore.CLIENT_S3])
        self.selected_bot_dirname = None
        self.selected_bot_dirpath = None

    def generate_audio_contents_from_texts(self):
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
                for i_bot, bot_folder in enumerate(bots_dirnames):
                    click.echo(f"{bot_folder} - {i_bot + 1}")

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

                current_content_element.id = text_element_safedict.get("id").to_str(default=None)
                current_content_element.created_by = text_element_safedict.get("createdBy").to_str(default=None)
                current_content_element.created_on = text_element_safedict.get("createdOn").to_str(default=None)
                current_content_element.modified_on = text_element_safedict.get("modifiedOn").to_str(default=None)
                content_elements.append(current_content_element)

            return content_elements

    @staticmethod
    def prompt_get_root_dirpath_to_save_audio() -> str:
        user_need_to_select_need_root_dirpath = False
        root_dirpath_to_save_audio_project = CliCache().cache().get("root_dirpath_to_save_audio_project").to_str(default=None)
        if root_dirpath_to_save_audio_project is not None:
            if not click.confirm(f"Do you want to save your audio files and folder to the following dirpath : {root_dirpath_to_save_audio_project}"):
                user_need_to_select_need_root_dirpath = True
        else:
            user_need_to_select_need_root_dirpath = True

        if user_need_to_select_need_root_dirpath is True:
            def prompt_user_to_select_root_dirpath_to_save_audio_project():
                return click.prompt(
                    text="To which dirpath to you wish to save all of the files and folders that will contain your audio ?",
                    type=str)

            root_dirpath_to_save_audio_project = prompt_user_to_select_root_dirpath_to_save_audio_project()
            while not os.path.isdir(root_dirpath_to_save_audio_project):
                if click.confirm(
                        f"The dirpath {root_dirpath_to_save_audio_project} did not exist. Do you want to create it ?"):
                    os.makedirs(root_dirpath_to_save_audio_project)
                else:
                    root_dirpath_to_save_audio_project = prompt_user_to_select_root_dirpath_to_save_audio_project()

            CliCache().cache().put("root_dirpath_to_save_audio_project", root_dirpath_to_save_audio_project)
            CliCache().save_cache_to_yaml()

        return root_dirpath_to_save_audio_project

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
        # todo: add possibility to set the character names and their voices
        root_dirpath_to_save_audio_project = self.prompt_get_root_dirpath_to_save_audio()

        for content_element in content_elements[400:]:
            if isinstance(content_element.dialogues_lines, list) and len(content_element.dialogues_lines) > 0:
                if content_element.id is None:
                    click.echo(f"Warning ! The content element with the following lines : "
                               f"{content_element.dialogues_lines.__dict__} did not had an id, and has not been saved.")
                else:
                    current_project_dirpath = os.path.join(root_dirpath_to_save_audio_project, content_element.id)
                    audacity_project_filepath = os.path.join(current_project_dirpath, f"{content_element.id}_project.aup")
                    wav_final_render_filepath = os.path.join(current_project_dirpath, "final_render.wav")
                    compressed_final_render_filepath = os.path.join(current_project_dirpath, "compressed_final_render.mp3")

                    # client.audacity.new_project()

                    client.synthesize_dialogues_lines_to_project(dialogues_lines=content_element.dialogues_lines,
                                                                 dirpath_to_save_to=current_project_dirpath)

                    client.audacity.save_project(project_output_filepath=audacity_project_filepath)
                    client.audacity.select_all()
                    client.audacity.export(filepath=wav_final_render_filepath)

                    from pydub import AudioSegment
                    final_render_audio_segment = AudioSegment.from_file(file=wav_final_render_filepath, format="wav", frame_rate=16000)
                    final_render_audio_segment.export(out_f=compressed_final_render_filepath, format="mp3", bitrate="48k")

                    print("done")
                    input()

    def upload_audio_contents(self):
        bucket_name = "test-vocal-export-inoft"
        region_name = "eu-west-3"

        root_dirpath_to_save_audio_project = self.prompt_get_root_dirpath_to_save_audio()
        for root, dirs, files in os.walk(root_dirpath_to_save_audio_project):
            for name in files:
                current_filepath = os.path.join(root, name)
                s3_object_key_name = current_filepath.replace(f"{root_dirpath_to_save_audio_project}\\", "")
                self.upload_to_s3(filepath=current_filepath, object_key_name=s3_object_key_name,
                                  bucket_name=bucket_name, region_name=region_name)
                print(f"Uploaded {current_filepath} to S3 : {bucket_name}/{s3_object_key_name}")




if __name__ == "__main__":
    # BotpressCore().generate_audio_contents_from_texts()
    BotpressCore().upload_audio_contents()
