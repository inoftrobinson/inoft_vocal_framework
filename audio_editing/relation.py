from inoft_vocal_framework.exceptions import raise_if_variable_not_expected_type, raise_if_variable_not_expected_type_and_not_none


class RelationProps:
    def __init__(self):
        self._parent_sound = None
        self._seconds_child_start_after_parent_start = None
        self._seconds_child_start_after_parent_end = None
        self._seconds_child_start_after_parent_start = None
        self._seconds_child_end_after_parent_end = None

    @property
    def parent_sound(self):
        return self._parent_sound

    @parent_sound.setter
    def parent_sound(self, parent_sound) -> None:
        self._parent_sound = parent_sound

    @property
    def seconds_child_start_after_parent_start(self) -> int:
        return self._seconds_child_start_after_parent_start

    @seconds_child_start_after_parent_start.setter
    def seconds_child_start_after_parent_start(self, seconds_child_start_after_parent_start: int) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=seconds_child_start_after_parent_start, expected_type=int,
                                                         variable_name="seconds_child_start_after_parent_start")
        self._seconds_child_start_after_parent_start = seconds_child_start_after_parent_start

    @property
    def seconds_child_start_after_parent_end(self) -> int:
        return self._seconds_child_start_after_parent_end

    @seconds_child_start_after_parent_end.setter
    def seconds_child_start_after_parent_end(self, seconds_child_start_after_parent_end: int) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=seconds_child_start_after_parent_end, expected_type=int,
                                                         variable_name="seconds_child_start_after_parent_end")
        self._seconds_child_start_after_parent_end = seconds_child_start_after_parent_end

    @property
    def seconds_child_start_after_parent_end(self) -> int:
        return self._seconds_child_start_after_parent_end

    @seconds_child_start_after_parent_end.setter
    def seconds_child_start_after_parent_end(self, seconds_child_start_after_parent_end: int) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=seconds_child_start_after_parent_end, expected_type=int,
                                                         variable_name="seconds_child_start_after_parent_end")
        self._seconds_child_start_after_parent_end = seconds_child_start_after_parent_end

    @property
    def seconds_child_end_after_parent_end(self) -> int:
        return self._seconds_child_end_after_parent_end

    @seconds_child_end_after_parent_end.setter
    def seconds_child_end_after_parent_end(self, seconds_child_end_after_parent_end: int) -> None:
        raise_if_variable_not_expected_type_and_not_none(value=seconds_child_end_after_parent_end, expected_type=int,
                                                         variable_name="seconds_child_end_after_parent_end")
        self._seconds_child_end_after_parent_end = seconds_child_end_after_parent_end


class Relation(RelationProps):
    def __init__(self, parent_sound, seconds_child_start_after_parent_start: float = None, seconds_child_start_after_parent_end: float = None,
                 seconds_child_end_after_parent_start: float = None, seconds_child_end_after_parent_end: float = None):
        super().__init__()
        self.parent_sound = parent_sound

        self.seconds_child_start_after_parent_start = seconds_child_start_after_parent_start
        self.seconds_child_start_after_parent_end = seconds_child_start_after_parent_end
        self.seconds_child_end_after_parent_start = seconds_child_end_after_parent_start
        self.seconds_child_end_after_parent_end = seconds_child_end_after_parent_end
        grouped_events = {"seconds_child_start_after_parent_start": self.seconds_child_start_after_parent_start,
                          "seconds_child_start_after_parent_end": self.seconds_child_start_after_parent_end,
                          "seconds_child_end_after_parent_start": self.seconds_child_end_after_parent_start,
                          "seconds_child_end_after_parent_end": self.seconds_child_end_after_parent_end}
        if self._count_times_value_in_list_not_none(grouped_events) > 1:
            raise Exception(f"For every relation, you can  set a value on only one of the following events {grouped_events}")

    @staticmethod
    def _count_times_value_in_list_not_none(list_or_dict) -> int:
        list_object = list_or_dict if isinstance(list_or_dict, list) else (list_or_dict.values() if isinstance(list_or_dict, dict) else list())
        count = 0
        for item in list_object:
            if item is not None:
                count += 1
        return count


