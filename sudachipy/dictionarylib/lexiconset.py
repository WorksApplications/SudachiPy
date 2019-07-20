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

from typing import List

from .lexicon import Lexicon


class LexiconSet(Lexicon):

    __MAX_DICTIONARIES = 16

    def __init__(self, system_lexicon: Lexicon):
        self.lexicons = [system_lexicon]
        self.pos_offsets = [0]

    def add(self, lexicon: Lexicon, pos_offset: int) -> None:
        if lexicon not in self.lexicons:
            self.lexicons.append(lexicon)
            self.pos_offsets.append(pos_offset)

    def is_full(self) -> bool:
        return len(self.lexicons) >= self.__MAX_DICTIONARIES

    def lookup(self, text: str, offset: int) -> Lexicon.Itr:
        if len(self.lexicons) == 1:
            return self.lexicons[0].lookup(text, offset)
        return self.__lookup(text, offset)

    def __lookup(self, text: str, offset: int) -> Lexicon.Itr:
        indices = list(range(len(self.lexicons)))[1:] + [0]
        for dict_id in indices:
            pairs = self.lexicons[dict_id].lookup(text, offset)
            for pair in pairs:
                yield (self.build_word_id(dict_id, pair[0]), pair[1])

    def get_left_id(self, word_id: int) -> int:
        return self.lexicons[self.get_dictionary_id(word_id)]\
            .get_left_id(self.get_word_id1(word_id))

    def get_right_id(self, word_id: int) -> int:
        return self.lexicons[self.get_dictionary_id(word_id)]\
            .get_right_id(self.get_word_id1(word_id))

    def get_cost(self, word_id: int) -> int:
        return self.lexicons[self.get_dictionary_id(word_id)]\
            .get_cost(self.get_word_id1(word_id))

    def get_word_info(self, word_id: int) -> 'WordInfo':  # noqa: F821
        dic_id = self.get_dictionary_id(word_id)
        winfo = self.lexicons[dic_id].get_word_info(self.get_word_id1(word_id))
        pos_id = winfo.pos_id
        if dic_id > 0 and pos_id >= self.pos_offsets[1]:  # user defined part-of-speech
            winfo.pos_id = winfo.pos_id - self.pos_offsets[1] + self.pos_offsets[dic_id]
        winfo.a_unit_split = self.convert_split(winfo.a_unit_split, dic_id)
        winfo.b_unit_split = self.convert_split(winfo.b_unit_split, dic_id)
        winfo.word_structure = self.convert_split(winfo.word_structure, dic_id)
        return winfo

    def get_dictionary_id(self, word_id: int) -> int:
        return word_id >> 28

    @staticmethod
    def get_word_id1(word_id: int) -> int:
        return 0x0FFFFFFF & word_id

    def get_word_id(self, headword: str, pos_id: int, reading_form: str) -> int:
        for dic_id in range(len(self.lexicons)):
            wid = self.lexicons[dic_id].get_word_id(headword, pos_id, reading_form)
            if wid <= 0:
                return self.build_word_id(dic_id, wid)
        return self.lexicons[0].get_word_id(headword, pos_id, reading_form)

    def build_word_id(self, dict_id, word_id):
        if word_id > 0x0FFFFFFF:
            raise AttributeError("word ID is too large: ", word_id)
        if dict_id > len(self.lexicons):
            raise AttributeError("dictionary ID is too large: ", dict_id)
        return (dict_id << 28) | word_id

    def size(self) -> int:
        return sum([lex.size() for lex in self.lexicons])

    def convert_split(self, split: List[int], dict_id: int) -> List[int]:
        for i in range(len(split)):
            if self.get_dictionary_id(split[i]) > 0:
                split[i] = self.build_word_id(dict_id, self.get_word_id1(split[i]))
        return split
