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
import unittest

from sudachipy.dictionarylib import SYSTEM_DICT_VERSION
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader


class TestDictionaryHeader(unittest.TestCase):

    def setUp(self):
        # Copied from sudachipy.dictionay.Dictionary.read_system_dictionary
        test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')
        filename = os.path.join(test_resources_dir, 'system.dic')
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        offset = 0
        self.header = DictionaryHeader.from_bytes(bytes_, offset)

    def test_version(self):
        self.assertEqual(SYSTEM_DICT_VERSION, self.header.version)

    def test_create_time(self):
        self.assertTrue(self.header.create_time > 0)

    def test_description(self):
        self.assertEqual("the system dictionary for the unit tests", self.header.description)


if __name__ == '__main__':
    unittest.main()
