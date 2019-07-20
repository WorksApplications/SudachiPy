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


class Grammar:
    INHIBITED_CONNECTION = 0x7fff

    def __init__(self, bytes_, offset):
        self.POS_DEPTH = 6
        self.BOS_PARAMETER = [0, 0, 0]
        self.EOS_PARAMETER = [0, 0, 0]

        self.char_category = None

        original_offset = offset
        self.bytes = bytes_
        self.connect_table_bytes = bytes_
        self.is_copied_connect_table = False
        pos_size = self.bytes_get_short(bytes_, offset)
        offset += 2
        self.pos_list = []

        for i in range(pos_size):
            pos = []
            for j in range(self.POS_DEPTH):
                pos.append(self.buffer_to_string(offset))
                offset += 1 + 2 * len(pos[j])
            self.pos_list.append(pos)
        self.left_id_size = self.bytes_get_short(bytes_, offset)
        offset += 2
        self.right_id_size = self.bytes_get_short(bytes_, offset)
        offset += 2
        self.connect_table_offset = offset

        self.storage_size = (offset - original_offset) + 2 * self.left_id_size * self.right_id_size

    def get_storage_size(self):
        return self.storage_size

    def get_part_of_speech_size(self):
        return len(self.pos_list)

    def get_part_of_speech_string(self, pos_id):
        return self.pos_list[pos_id]

    def get_part_of_speech_id(self, pos):
        return self.pos_list.index(pos) if pos in self.pos_list else -1

    def get_connect_cost(self, left_id: int, right_id: int) -> int:
        return self.bytes_get_short(self.connect_table_bytes, self.connect_table_offset + 2 * left_id + 2 * self.left_id_size * right_id)

    def set_connect_cost(self, left_id, right_id, cost):
        # bytes_ must be ACCESS_COPY mode
        self.bytes_put_short(self.connect_table_bytes, self.connect_table_offset + 2 * left_id + 2 * self.left_id_size * right_id, cost)

    def get_bos_parameter(self):
        return self.BOS_PARAMETER

    def get_eos_parameter(self):
        return self.EOS_PARAMETER

    def get_character_category(self):
        return self.char_category

    def set_character_category(self, char_category):
        self.char_category = char_category

    def buffer_to_string(self, offset):
        self.bytes.seek(offset)
        length = self.bytes.read_byte()
        offset += 1
        string = self.bytes.read(2 * length)
        return string.decode('utf-16')

    @staticmethod
    def bytes_get_short(bytes_, offset):
        bytes_.seek(offset)
        return int.from_bytes(bytes_.read(2), 'little', signed=True)

    @staticmethod
    def bytes_put_short(bytes_, offset, data):
        bytes_.seek(offset)
        bytes_.write(data.to_bytes(2, 'little'))

    def add_pos_list(self, grammar):
        self.pos_list.extend(grammar.pos_list)
