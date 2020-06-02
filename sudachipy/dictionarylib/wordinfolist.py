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

import struct
from functools import lru_cache

from .wordinfo import WordInfo


class WordInfoList(object):
    def __init__(self, bytes_, offset, word_size):
        self.bytes = bytes_
        self.offset = offset
        self._word_size = word_size

    @lru_cache(2048)
    def get_word_info(self, word_id):
        orig_pos = self.bytes.tell()
        index = self.word_id_to_offset(word_id)
        self.bytes.seek(index)
        surface = self.buffer_to_string()
        head_word_length = self.buffer_to_string_length()
        pos_id = int.from_bytes(self.bytes.read(2), 'little')
        normalized_form = self.buffer_to_string()
        if not normalized_form:
            normalized_form = surface
        dictionary_form_word_id = int.from_bytes(self.bytes.read(4), 'little', signed=True)
        reading_form = self.buffer_to_string()
        if not reading_form:
            reading_form = surface
        a_unit_split = self.buffer_to_int_array()
        b_unit_split = self.buffer_to_int_array()
        word_structure = self.buffer_to_int_array()

        dictionary_form = surface
        if dictionary_form_word_id >= 0 and dictionary_form_word_id != word_id:
            wi = self.get_word_info(dictionary_form_word_id)
            dictionary_form = wi.surface

        self.bytes.seek(orig_pos)

        return WordInfo(surface, head_word_length, pos_id, normalized_form, dictionary_form_word_id,
                        dictionary_form, reading_form, a_unit_split, b_unit_split, word_structure)

    def word_id_to_offset(self, word_id):
        i = self.offset + 4 * word_id
        return int.from_bytes(self.bytes[i:i + 4], 'little', signed=False)

    def buffer_to_string_length(self):
        length = self.bytes.read_byte()
        if length < 128:
            return length
        low = self.bytes.read_byte()
        return ((length & 0x7F) << 8) | low

    def buffer_to_string(self):
        length = self.buffer_to_string_length()
        return self.bytes.read(2 * length).decode('utf-16-le')

    def buffer_to_int_array(self):
        length = self.bytes.read_byte()
        _bytes = self.bytes.read(4 * length)
        return list(struct.unpack('{}i'.format(length), _bytes))

    def size(self):
        return self._word_size
