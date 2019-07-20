# Copyright (c) 2019 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
