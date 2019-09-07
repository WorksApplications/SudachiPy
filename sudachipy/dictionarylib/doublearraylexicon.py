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

import mmap

from dartsclone import DoubleArray

from . import wordidtable
from . import wordinfolist
from . import wordparameterlist
from .lexicon import Lexicon


class DoubleArrayLexicon(Lexicon):

    __SIGNED_SHORT_MIN = -32768
    __SIGNED_SHORT_MAX = 32767
    __USER_DICT_COST_PER_MORPH = -20

    trie = None
    word_id_table = None
    word_params = None

    def __init__(self, bytes_: mmap.mmap, offset: int):
        self.trie = DoubleArray()
        bytes_.seek(offset)
        size = int.from_bytes(bytes_.read(4), 'little')
        offset += 4

        array = memoryview(bytes_)[offset:offset + size * 4]
        self.trie.set_array(array, size)
        offset += self.trie.total_size()

        self.word_id_table = wordidtable.WordIdTable(bytes_, offset)
        offset += self.word_id_table.storage_size()

        self.word_params = wordparameterlist.WordParameterList(bytes_, offset)
        offset += self.word_params.storage_size()

        self.word_infos = wordinfolist.WordInfoList(bytes_, offset, self.word_params.get_size())

    def __del__(self):
        del self.word_params

    def lookup(self, text: bytes, offset: int) -> Lexicon.Itr:
        key = text[offset:]
        result = self.trie.common_prefix_search(key, length=len(key))
        for index, length in result:
            word_ids = self.word_id_table.get(index)
            length += offset
            for word_id in word_ids:
                yield (word_id, length)

    def get_left_id(self, word_id: int) -> int:
        return self.word_params.get_left_id(word_id)

    def get_right_id(self, word_id: int) -> int:
        return self.word_params.get_right_id(word_id)

    def get_cost(self, word_id: int) -> int:
        return self.word_params.get_cost(word_id)

    def get_word_info(self, word_id: int) -> 'WordInfo':  # noqa: F821
        return self.word_infos.get_word_info(word_id)

    def size(self) -> int:
        return self.word_params.size

    def get_word_id(self, headword: str, pos_id: int, reading_form: str) -> int:
        for wid in range(self.word_infos.size()):
            info = self.word_infos.get_word_info(wid)
            if info.surface == headword \
                    and info.pos_id == pos_id \
                    and info.reading_form == reading_form:
                return wid
        return -1

    def get_dictionary_id(self, word_id: int) -> int:
        return 0

    def calculate_cost(self, tokenizer) -> None:
        for wid in range(self.word_params.size):
            if self.get_cost(wid) != self.__SIGNED_SHORT_MIN:
                continue
            surface = self.get_word_info(wid).surface
            ms = tokenizer.tokenize(surface, None)
            cost = ms.get_internal_cost() + self.__USER_DICT_COST_PER_MORPH * len(ms)
            cost = min(cost, self.__SIGNED_SHORT_MAX)
            cost = max(cost, self.__SIGNED_SHORT_MIN)
            self.word_params.set_cost(wid, cost)
