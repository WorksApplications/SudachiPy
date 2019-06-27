from abc import ABC, abstractmethod
from typing import Iterator, List

from .wordinfo import WordInfo


class Lexicon(ABC):

    Itr = Iterator[List[int]]

    @abstractmethod
    def lookup(self, text: str, offset: int) -> Itr:  # noqa: F821
        raise NotImplementedError

    @abstractmethod
    def get_word_id(self, headword: str, pos_id: int, reading_form: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_left_id(self, word_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_right_id(self, word_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_cost(self, word_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_word_info(self, word_id: int) -> 'WordInfo':
        raise NotImplementedError

    @abstractmethod
    def get_dictionary_id(self, word_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError
