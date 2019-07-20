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

import mmap
import os
import shutil
import tempfile
import unittest

from sudachipy.dictionarylib.grammar import Grammar


class TestGrammar(unittest.TestCase):

    alloc_size = 4096

    def setUp(self):
        storage = bytearray()
        self.build_partofspeech(storage)
        self.build_connect_table(storage)
        self.test_dir = tempfile.mkdtemp()
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'wb') as wf:
            wf.write(bytes(storage))
        self.mmap = None
        with open(f, 'rb') as rf:
            self.mmap = mmap.mmap(rf.fileno(), 0, access=mmap.ACCESS_COPY)
        self.storage_size = self.mmap.size()
        offset = 0
        self.grammar = Grammar(self.mmap, offset)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_storage_size(self):
        self.assertEqual(self.storage_size, self.grammar.storage_size)

    def test_get_partofspeech_string(self):
        self.assertEqual(6, len(self.grammar.get_part_of_speech_string(0)))
        self.assertEqual("BOS/EOS", self.grammar.get_part_of_speech_string(0)[0])
        self.assertEqual("*", self.grammar.get_part_of_speech_string(0)[5])

        self.assertEqual("一般", self.grammar.get_part_of_speech_string(1)[1])
        self.assertEqual("*", self.grammar.get_part_of_speech_string(1)[5])

        self.assertEqual("五段-サ行", self.grammar.get_part_of_speech_string(2)[4])
        self.assertEqual("終止形-一般", self.grammar.get_part_of_speech_string(2)[5])

    def test_get_connect_cost(self):
        self.assertEqual(0, self.grammar.get_connect_cost(0, 0))
        self.assertEqual(-100, self.grammar.get_connect_cost(2, 1))
        self.assertEqual(200, self.grammar.get_connect_cost(1, 2))

    def test_set_connect_cost(self):
        self.grammar.set_connect_cost(0, 0, 300)
        self.assertEqual(300, self.grammar.get_connect_cost(0, 0))

    def test_get_bos_parameters(self):
        self.assertEqual(0, self.grammar.get_bos_parameter()[0])
        self.assertEqual(0, self.grammar.get_bos_parameter()[1])
        self.assertEqual(0, self.grammar.get_bos_parameter()[2])

    def test_get_eos_parameters(self):
        self.assertEqual(0, self.grammar.get_eos_parameter()[0])
        self.assertEqual(0, self.grammar.get_eos_parameter()[1])
        self.assertEqual(0, self.grammar.get_eos_parameter()[2])

    def test_read_from_file(self):
        # Todo
        # after tidying up dictionary management
        pass

    @staticmethod
    def build_partofspeech(storage):
        storage.extend((3).to_bytes(2, byteorder='little', signed=True))  # number of part of speech

        storage.extend(b'\x07B\x00O\x00S\x00/\x00E\x00O\x00S\x00\x01*\x00\x01*\x00\x01*\x00\x01*\x00\x01*\x00')

        storage.extend(b'\x02')
        storage.extend('名刺'.encode('utf-16-le'))
        storage.extend(b'\x02')
        storage.extend('一般'.encode('utf-16-le'))
        storage.extend(b'\x01*\x00\x01*\x00\x01*\x00\x01*\x00')

        storage.extend(b'\x02')
        storage.extend('動詞'.encode('utf-16-le'))
        storage.extend(b'\x02')
        storage.extend('一般'.encode('utf-16-le'))
        storage.extend(b'\x01*\x00\x01*\x00\x05')
        storage.extend('五段-サ行'.encode('utf-16-le'))
        storage.extend(b'\x06')
        storage.extend('終止形-一般'.encode('utf-16-le'))

    @staticmethod
    def build_connect_table(storage):
        storage.extend((3).to_bytes(2, byteorder='little', signed=True))  # number of leftId
        storage.extend((3).to_bytes(2, byteorder='little', signed=True))  # number of rightId

        storage.extend((0).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((-300).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((3000).to_bytes(2, byteorder='little', signed=True))  # number of rightId

        storage.extend((300).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((-500).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((-100).to_bytes(2, byteorder='little', signed=True))  # number of frightId

        storage.extend((-3000).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((200).to_bytes(2, byteorder='little', signed=True))  # number of rightId
        storage.extend((2000).to_bytes(2, byteorder='little', signed=True))  # number of rightId


if __name__ == '__main__':
    unittest.main()
