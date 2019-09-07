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


class WordIdTable(object):
    def __init__(self, bytes_, offset):
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')
        self.offset = offset + 4
        self._bytes_view = memoryview(bytes_)[self.offset: self.offset + self.size]

    def __del__(self):
        self._bytes_view.release()

    def storage_size(self):
        return 4 + self.size

    def get(self, index):
        length = self._bytes_view[index]
        result = struct.unpack_from("<{}I".format(length), self._bytes_view, index + 1)
        return result
