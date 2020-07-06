from inoft_vocal_engine.exceptions import raise_if_variable_not_expected_type, raise_if_variable_not_expected_type_and_not_none


class ContentElement:
    def __init__(self, id_value: str = None, created_by: str = None, created_on: str = None, modified_on: str = None, dialogues_lines: list = None):
        self.id = id_value
        self.created_by = created_by
        self.created_on = created_on
        self.modified_on = modified_on
        self.dialogues_lines = dialogues_lines

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id_value: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=id_value, expected_type=str, variable_name="id")
        self._id = id_value

    @property
    def created_by(self) -> str:
        return self._created_by

    @created_by.setter
    def created_by(self, created_by: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=created_by, expected_type=str, variable_name="created_by")
        self._created_by = created_by

    @property
    def created_on(self) -> str:
        return self._created_on

    @created_on.setter
    def created_on(self, created_on: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=created_on, expected_type=str, variable_name="created_on")
        self._created_on = created_on

    @property
    def modified_on(self) -> str:
        return self._modified_on

    @modified_on.setter
    def modified_on(self, modified_on: str) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=modified_on, expected_type=str, variable_name="modified_on")
        self._modified_on = modified_on

    @property
    def dialogues_lines(self) -> list:
        return self._dialogues_lines

    @dialogues_lines.setter
    def dialogues_lines(self, dialogues_lines: list) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=dialogues_lines, expected_type=list, variable_name="dialogues_lines")
        self._dialogues_lines = dialogues_lines
