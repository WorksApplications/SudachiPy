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

from .dictionarylib.wordinfo import WordInfo

__NULL_SURFACE = '(null)'
UNK = WordInfo(__NULL_SURFACE, 0, -1, __NULL_SURFACE, -1,
               __NULL_SURFACE, __NULL_SURFACE, [], [], [])


class LatticeNode:

    begin = 0
    end = 0
    total_cost = 0
    word_id = 0
    _is_oov = False
    best_previous_node = None
    is_connected_to_bos = None
    extra_word_info = None
    lexicon = None
    left_id = None
    right_id = None
    cost = None

    def __init__(self, lexicon=None, left_id=None, right_id=None, cost=None, word_id=None):

        self.is_defined = True
        if lexicon is left_id is right_id is cost is word_id is None:
            self.is_defined = False
            return
        self.lexicon = lexicon
        self.left_id = left_id
        self.right_id = right_id
        self.cost = cost
        self.word_id = word_id

    def set_parameter(self, left_id: int, right_id: int, cost: int) -> None:
        self.left_id = left_id
        self.right_id = right_id
        self.cost = cost

    def get_begin(self) -> int:
        return self.begin

    def get_end(self) -> int:
        return self.end

    def set_range(self, begin: int, end: int) -> None:
        self.begin = begin
        self.end = end

    def is_oov(self):
        return self._is_oov

    def set_oov(self):
        self._is_oov = True

    def get_word_info(self) -> WordInfo:
        if not self.is_defined:
            return UNK
        if self.extra_word_info:
            return self.extra_word_info
        return self.lexicon.get_word_info(self.word_id)

    def set_word_info(self, word_info: WordInfo) -> None:
        self.extra_word_info = word_info
        self.is_defined = True

    def get_path_cost(self) -> int:
        return self.cost

    def get_word_id(self) -> int:
        return self.word_id

    def get_dictionary_id(self) -> int:
        if not self.is_defined or self.extra_word_info:
            return -1
        return self.lexicon.get_dictionary_id(self.word_id)  # self.word_id >> 28

    def __str__(self):
        surface = "(None)"
        if self.word_id >= 0 or self.extra_word_info:
            surface = self.get_word_info().surface

        return "{} {} {}({}) {} {} {}".format(
            self.get_begin(), self.get_end(), surface, self.word_id, self.left_id, self.right_id, self.cost
        )
