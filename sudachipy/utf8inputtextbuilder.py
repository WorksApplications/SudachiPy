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

import copy

from . import utf8inputtext
from .dictionarylib.categorytype import CategoryType


class UTF8InputTextBuilder:
    def __init__(self, text, grammar):

        self.grammar = grammar
        self.original_text = text
        self.modified_text = text
        self.modified_to_original = list(range(len(self.original_text) + 1))
        # 注: サロゲートペア文字は考慮していない

    def replace(self, begin, end, str_):
        if begin < 0:
            raise IndexError(begin)
        if begin > len(self.modified_text):
            raise IndexError("begin > length")
        if begin > end:
            raise IndexError("begin > end")
        if begin == end:
            raise AttributeError("begin == end")

        if end > len(self.modified_text):
            end = len(self.modified_text)

        self.modified_text = str_.join([self.modified_text[:begin], self.modified_text[end:]])

        modified_begin = self.modified_to_original[begin]
        modified_end = self.modified_to_original[end]
        length = len(str_)
        if end - begin > length:
            del self.modified_to_original[begin + length:end]
        self.modified_to_original[begin] = modified_begin
        for i in range(1, length):
            if begin + i < end:
                self.modified_to_original[begin + i] = modified_end
            else:
                self.modified_to_original.insert(begin + i, modified_end)

    def get_original_text(self):
        return self.original_text

    def get_text(self):
        return self.modified_text

    def build(self):
        modified_string_text = self.get_text()
        byte_text = modified_string_text.encode('utf-8')

        length = len(byte_text)
        byte_indexes = [0 for i in range(length + 1)]
        offsets = [0 for i in range(length + 1)]
        j = 0
        for i in range(len(self.modified_text)):
            # 注: サロゲートペア文字は考慮していない
            for _ in range(self.utf8_byte_length(ord(self.modified_text[i]))):
                byte_indexes[j] = i
                offsets[j] = self.modified_to_original[i]
                j += 1
        byte_indexes[length] = len(modified_string_text)
        offsets[length] = self.modified_to_original[-1]

        char_categories = self.get_char_category_types(modified_string_text)
        char_category_continuities = self.get_char_category_continuities(modified_string_text, length, char_categories)
        can_bow_list = self._build_can_bow_list(modified_string_text, char_categories)
        return utf8inputtext.UTF8InputText(
            self.grammar, self.original_text, modified_string_text, byte_text,
            offsets, byte_indexes, char_categories, char_category_continuities, can_bow_list)

    def get_char_category_types(self, text):
        return [self.grammar.get_character_category().get_category_types(ord(c)) for c in text]

    def get_char_category_continuities(self, text, byte_length, char_categories):
        if len(text) == 0:
            return []
        char_category_continuities = []
        i = 0
        while i < len(char_categories):
            next_ = i + self.get_char_category_continuous_length(char_categories, i)
            length = 0
            for j in range(i, next_):
                length += self.utf8_byte_length(ord(text[j]))
            for k in range(length, 0, -1):
                char_category_continuities.append(k)
            i = next_
        return char_category_continuities

    def get_char_category_continuous_length(self, char_categories, offset):
        continuous_category = copy.deepcopy(char_categories[offset])
        for length in range(1, len(char_categories) - offset):
            continuous_category = continuous_category & char_categories[offset + length]
            if len(continuous_category) == 0:
                return length
        return len(char_categories) - offset

    def utf8_byte_length(self, cp):
        if cp < 0:
            return 0
        elif cp <= 0x7F:
            return 1
        elif cp <= 0x7FF:
            return 2
        elif cp <= 0xFFFF:
            return 3
        elif cp <= 0x10FFFF:
            return 4
        else:
            return 0

    def _build_can_bow_list(self, text, char_categories):
        if not text:
            return []
        can_bow_list = []
        for i, cat in enumerate(char_categories):
            if i == 0:
                can_bow_list.append(True)
                continue

            if CategoryType.ALPHA in cat or CategoryType.GREEK in cat or CategoryType.CYRILLIC in cat:
                types = cat & char_categories[i - 1]
                can_bow_list.append(not bool(types))
                continue

            can_bow_list.append(True)

        return can_bow_list
