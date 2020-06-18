# cython: profile=True

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
UNK =\
    WordInfo(__NULL_SURFACE, 0, -1, __NULL_SURFACE, -1,
             __NULL_SURFACE, __NULL_SURFACE, [], [], [])

cdef class LatticeNode:

    def __init__(self, lexicon=None, left_id=None, right_id=None, cost=None, word_id=None):

        self.begin = 0
        self.end = 0
        self.word_id = 0
        self._is_oov = False
        self.best_previous_node = None
        self.is_connected_to_bos = False
        self.extra_word_info = None

        self._is_defined = True
        if lexicon is left_id is right_id is cost is word_id is None:
            self._is_defined = False
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

    def set_begin(self, begin) -> None:
        self.begin = begin

    def get_end(self) -> int:
        return self.end

    def set_end(self, end) -> None:
        self.end = end

    def set_range(self, begin: int, end: int) -> None:
        self.begin = begin
        self.end = end

    def is_oov(self):
        return self._is_oov

    def set_oov(self):
        self._is_oov = True
    
    def is_defined(self):
        return self._is_defined
    
    def set_defined(self):
        self._is_defined = True
    
    def get_word_info(self) -> WordInfo:
        if not self._is_defined:
            return UNK
        if self.extra_word_info:
            return self.extra_word_info
        return self.lexicon.get_word_info(self.word_id)

    def set_word_info(self, word_info: WordInfo) -> None:
        self.extra_word_info = word_info
        self._is_defined = True

    def get_path_cost(self) -> int:
        return self.cost
    
    def get_left_id(self) -> int:
        return self.left_id
    
    def get_right_id(self) -> int:
        return self.right_id

    def get_word_id(self) -> int:
        return self.word_id

    def get_dictionary_id(self) -> int:
        if not self._is_defined or self.extra_word_info:
            return -1
        return self.lexicon.get_dictionary_id(self.word_id)  # self.word_id >> 28

    def __str__(self):
        surface = "(None)"
        if self.word_id >= 0 or self.extra_word_info:
            surface = self.get_word_info().surface

        return "{} {} {}({}) {} {} {}".format(
            self.get_begin(), self.get_end(), surface, self.word_id, self.left_id, self.right_id, self.cost
        )
