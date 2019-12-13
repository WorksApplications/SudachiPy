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


class UTF8InputText:
    def __init__(self, grammar, original_text, modified_text, bytes_, offsets, byte_indexes, char_categories, char_category_continuities, can_bow_list=None):
        self.original_text = original_text
        self.modified_text = modified_text
        self.bytes = bytes_
        self.offsets = offsets
        self.byte_indexes = byte_indexes
        self.char_categories = char_categories
        self.char_category_continuities = char_category_continuities
        self.can_bow_list = can_bow_list

    def get_original_text(self):
        return self.original_text

    def get_text(self):
        return self.modified_text

    def get_byte_text(self):
        return self.bytes

    def get_substring(self, begin, end):
        if begin < 0:
            raise IndexError(begin)
        if end > len(self.bytes):
            raise IndexError(end)
        if (begin > end):
            raise IndexError(end - begin)

        return self.modified_text[self.byte_indexes[begin]:self.byte_indexes[end]]

    def get_offset_text_length(self, index):
        return self.byte_indexes[index]

    def is_char_alignment(self, index):
        return (self.bytes[index] & 0xC0) != 0x80

    def get_original_index(self, index):
        return self.offsets[index]

    def get_char_category_types(self, begin, end=None):
        if end is None:
            return self.char_categories[self.byte_indexes[begin]]
        if begin + self.get_char_category_continuous_length(begin) < end:
            return []
        b = self.byte_indexes[begin]
        e = self.byte_indexes[end]
        continuous_category = copy.deepcopy(self.char_categories[b])
        for i in range(b + 1, e):
            continuous_category = continuous_category & self.char_categories[i]
        return continuous_category

    def get_char_category_continuous_length(self, index):
        return self.char_category_continuities[index]

    def get_code_points_offset_length(self, index, code_point_offset):
        length = 0
        target = self.byte_indexes[index] + code_point_offset
        for i in range(index, len(self.bytes)):
            if self.byte_indexes[i] >= target:
                return length
            length += 1
        return length

    def can_bow(self, idx: int) -> bool:
        return self.is_char_alignment(idx) and self.can_bow_list[self.byte_indexes[idx]]

    def code_point_count(self, begin: int, end: int):
        return self.byte_indexes[end] - self.byte_indexes[begin]

    def get_word_candidate_length(self, index):
        for i in range(index + 1, len(self.bytes)):
            if self.can_bow(i):
                return i - index
        return len(self.bytes) - index
