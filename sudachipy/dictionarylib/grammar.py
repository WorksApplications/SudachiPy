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
        self._POS_DEPTH = 6
        self._BOS_PARAMETER = [0, 0, 0]
        self._EOS_PARAMETER = [0, 0, 0]

        self.char_category = None
        self.is_copied_connect_table = False

        original_offset = bytes_.tell()
        bytes_.seek(offset)
        pos_size = self.bytes_get_short(bytes_)
        self.pos_list = []
        for i in range(pos_size):
            pos = []
            for j in range(self._POS_DEPTH):
                pos.append(self.bytes_get_string(bytes_))
            self.pos_list.append(pos)
        left_id_size = self.bytes_get_short(bytes_)
        right_id_size = self.bytes_get_short(bytes_)
        connect_table_offset = bytes_.tell()

        self.storage_size = (connect_table_offset - offset) + 2 * left_id_size * right_id_size

        self._matrix_view = \
            memoryview(bytes_)[connect_table_offset: connect_table_offset + 2 * left_id_size * right_id_size]
        if left_id_size * right_id_size != 0:
            self._matrix_view = self._matrix_view.cast('h', shape=[left_id_size, right_id_size])
        bytes_.seek(original_offset)

    def __del__(self):
        self._matrix_view.release()

    def get_storage_size(self):
        return self.storage_size

    def get_part_of_speech_size(self):
        return len(self.pos_list)

    def get_part_of_speech_string(self, pos_id):
        return self.pos_list[pos_id]

    def get_part_of_speech_id(self, pos):
        return self.pos_list.index(pos) if pos in self.pos_list else -1

    def get_connect_cost(self, left: int, right: int) -> int:
        """ Returns connection cost of nodes

        Args:
            left: right-ID of left node
            right: left-ID of right node

        Returns:
            cost of connection

        """
        return self._matrix_view[right, left]

    def set_connect_cost(self, left: int, right: int, cost: int) -> None:
        """ Sets connection cost of nodes

        Note: bytes_ must be ACCESS_COPY mode

        Args:
            left: right-ID of left node
            right: left-ID of right node
            cost: cost of connection

        """
        self._matrix_view[right, left] = cost

    def get_bos_parameter(self):
        return self._BOS_PARAMETER

    def get_eos_parameter(self):
        return self._EOS_PARAMETER

    def get_character_category(self):
        return self.char_category

    def set_character_category(self, char_category):
        self.char_category = char_category

    @staticmethod
    def bytes_get_string(bytes_):
        length = bytes_.read_byte()
        string = bytes_.read(2 * length)
        return string.decode('utf-16')

    @staticmethod
    def bytes_get_short(bytes_):
        return int.from_bytes(bytes_.read(2), 'little', signed=True)

    def add_pos_list(self, grammar):
        self.pos_list.extend(grammar.pos_list)
