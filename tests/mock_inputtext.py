from copy import deepcopy
from unittest import mock

from sudachipy.utf8inputtext import UTF8InputText


mocked_input_text = mock.Mock(spec=UTF8InputText)
text = ''
types = []


def set_text(text_: str) -> None:
    global text, types
    text = text_
    types = [set() for _ in text]


def set_category_type(begin: int, end: int, type_) -> None:
    global types
    for i in range(begin, end):
        types[i].add(type_)


mocked_input_text.get_text.return_value = text

mocked_input_text.get_original_text.return_value = text


def _mocked_get_substring(begin: int, end: int) -> str:
    global text
    return text[begin:end]


mocked_input_text.get_substring.side_effect = _mocked_get_substring


def _mocked_get_char_category_types(begin: int, end: int = None) -> set:
    global text, types
    if end is None:
        return types[begin]
    continuous_category = deepcopy(types[begin])
    for i in range(begin + 1, end):
        continuous_category = continuous_category.intersection(types[i])
    return continuous_category


mocked_input_text.get_char_category_types.side_effect = _mocked_get_char_category_types


def _mocked_get_char_category_continuous_length(idx: int) -> int:
    global text, types
    continuous_category = deepcopy(types[idx])
    for i in range(idx + 1, len(text)):
        continuous_category = continuous_category.intersection(types[i])
        if not continuous_category:
            return i - idx
    return len(text) - idx


mocked_input_text.get_char_category_continuous_length.side_effect = _mocked_get_char_category_continuous_length


def _mocked_get_code_points_offset_length(idx: int, offset: int) -> int:
    return offset


mocked_input_text.get_code_points_offset_length.side_effect = _mocked_get_code_points_offset_length
