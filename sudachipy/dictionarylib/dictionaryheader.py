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

from sudachipy.dictionarylib.jtypedbytebuffer import JTypedByteBuffer


class DictionaryHeader:

    __DESCRIPTION_SIZE = 256
    __STORAGE_SIZE = 8 + 8 + __DESCRIPTION_SIZE

    def __init__(self, version, create_time, description):
        self.version = version
        self.create_time = create_time
        self.description = description

    @classmethod
    def from_bytes(cls, bytes_, offset):
        version, create_time = struct.unpack_from("<2Q", bytes_, offset)
        offset += 16

        len_ = 0
        while len_ < cls.__DESCRIPTION_SIZE:
            if bytes_[offset + len_] == 0:
                break
            len_ += 1
        description = bytes_[offset:offset + len_].decode("utf-8")
        return cls(version, create_time, description)

    def to_bytes(self):
        buf = JTypedByteBuffer(b'\x00' * (16 + self.__DESCRIPTION_SIZE))
        buf.seek(0)
        buf.write_int(self.version, 'long', signed=False)
        buf.write_int(self.create_time, 'long')
        bdesc = self.description.encode('utf-8')
        if len(bdesc) > self.__DESCRIPTION_SIZE:
            raise ValueError('description is too long')
        buf.write(bdesc)
        return buf.getvalue()

    def storage_size(self):
        return self.__STORAGE_SIZE
