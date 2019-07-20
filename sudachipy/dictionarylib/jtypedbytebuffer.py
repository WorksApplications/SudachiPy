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

from io import BytesIO


class JTypedByteBuffer(BytesIO):
    """
    A interface of BytesIO to write dictionary
    """

    __ENDIAN = 'little'

    @classmethod
    def from_bytes(cls, bytes_io):
        return cls(bytes_io.getvalue())

    def write_int(self, int_, type_, signed=True):
        if type_ == 'byte':
            len_ = 1
            signed = False
        elif type_ == 'int':
            len_ = 4
        elif type_ == 'char':
            len_ = 2
            signed = False
        elif type_ == 'short':
            len_ = 2
        elif type_ == 'long':
            len_ = 8
        else:
            raise ValueError('{} is invalid type'.format(type_))
        self.write(int_.to_bytes(len_, byteorder=self.__ENDIAN, signed=signed))

    def write_str(self, text):
        self.write(text.encode('utf-16-le'))

    def clear(self):
        self.seek(0)
        self.truncate(0)
