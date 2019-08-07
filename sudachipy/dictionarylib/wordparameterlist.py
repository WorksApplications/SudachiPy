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


class WordParameterList(object):

    ELEMENT_SIZE = 2 * 3
    ELEMENT_SIZE_AS_SHORT = 3

    def __init__(self, bytes_, offset):
        original_offset = bytes_.tell()
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')
        array_offset = bytes_.tell()
        self._array_view = memoryview(bytes_)[array_offset: array_offset + self.size * self.ELEMENT_SIZE]
        self._array_view = self._array_view.cast('h')
        # self.is_copied = False
        bytes_.seek(original_offset)

    def __del__(self):
        self._array_view.release()

    def storage_size(self):
        return 4 + self.ELEMENT_SIZE * self.size

    def get_size(self):
        return self.size

    def get_left_id(self, word_id):
        return self._array_view[self.ELEMENT_SIZE_AS_SHORT * word_id]

    def get_right_id(self, word_id):
        return self._array_view[self.ELEMENT_SIZE_AS_SHORT * word_id + 1]

    def get_cost(self, word_id):
        return self._array_view[self.ELEMENT_SIZE_AS_SHORT * word_id + 2]

    def set_cost(self, word_id, cost):
        # bytes_ must be ACCESS_COPY mode
        self._array_view[self.ELEMENT_SIZE_AS_SHORT * word_id + 2] = cost
