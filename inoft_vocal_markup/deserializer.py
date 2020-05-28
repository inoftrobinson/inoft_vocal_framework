from typing import Optional, List

from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type


class DialogueLine:
    def __init__(self, character_name: str = None, line_content: str = None, additional_character_metadata: Optional[str] = None):
        self.character_name = character_name
        self.line_content = line_content
        self.additional_character_metadata = additional_character_metadata


class Deserializer:
    def __init__(self, characters_names: Optional[list] = None):
        self.characters_names = characters_names

    def deserialize(self, text: str) -> List[DialogueLine]:
        lines = text.split("\n")
        dialogues_lines: List[DialogueLine] = list()

        for line in lines:
            current_dialogue_line = DialogueLine()

            has_found_first_star_in_line = False
            text_to_find_first_character_name = ""
            has_found_character_name = False

            for i_char, char in enumerate(line):
                if has_found_first_star_in_line is True:
                    text_to_find_first_character_name += char

                if has_found_character_name is False:
                    for character_name in self.characters_names:
                        if character_name in text_to_find_first_character_name:
                            current_dialogue_line.character_name = character_name
                            has_found_character_name = True

                    if char == "*":
                        has_found_first_star_in_line = True

                elif has_found_character_name is True:
                    if char == "*":
                        # Has found a star after having found a character name. Which we means, we have reached the end
                        # of the declaration of which character is talking, like the following : *Jean-Michel* Hi my friend !

                        # We remove the last character from the text to find the character name (so that we remove the current star char).
                        # And we remove the character name from the text, we strip of any additional junk chars, and if we still have
                        # something, it means that between the two stars where the character name has been found, there was more infos
                        # than just the character name, it is the additional character metadata that we add to the current dialogue line.
                        metadata = text_to_find_first_character_name[:-1].replace(current_dialogue_line.character_name, "").strip()
                        if metadata != "":
                            current_dialogue_line.additional_character_metadata = metadata

                        # Then we can use the rest of the line as what the user has said, and we add 1 the i_char,
                        # to not include the star char, and strip the text to remove any potential trailing spaces.
                        line_content = line[i_char + 1:].strip()
                        if line_content != "":
                            current_dialogue_line.line_content = line_content
                        break

                if i_char == len(line) - 1:
                    # If the char has is the last char of the line, and that the loop has not been
                    # break after finding a character name, then we will not set the character
                    # name, and just put the entire line as the dialogue line content.
                    line_content = line.strip()
                    if line_content != "":
                        current_dialogue_line.line_content = line_content

            if current_dialogue_line.line_content is not None:
                dialogues_lines.append(current_dialogue_line)
            elif current_dialogue_line.character_name is not None or current_dialogue_line.additional_character_metadata is not None:
                print(f"Warning ! A dialogue line was not empty of infos, but its content was empty : {current_dialogue_line.__dict__}")

        for line in dialogues_lines:
            print(line.__dict__)

        return dialogues_lines


if __name__ == "__main__":
    text_ = "*Léo parlant fort * Willie, t'arrête pas, ont y est presque !\n*bruits de course recommence et s'arrête*\n*Menu* Vous êtes arrivé au camp, vous êtes à une dizaine de mètre de la tente de communication. Une voiture KubelWagen couleur sable se trouve à votre droite. Une grande roue est accroché sur le capeau, et une mitrailleuse est monté au milieu de la voiture. Elle est suffisamment haute pour que que vous puissiez vous cacher derrière ou même en dessous de leurs uniformes."
    Deserializer(characters_names=["Léo", "Willie", "Menu"]).deserialize(text=text_)