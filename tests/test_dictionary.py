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

import os
import unittest

from sudachipy import tokenizer
from sudachipy.dictionary import Dictionary


class TestDictionary(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.dict_ = Dictionary(os.path.join(resource_dir, 'sudachi.json'), resource_dir=resource_dir)

    def tearDown(self) -> None:
        self.dict_.close()

    def test_create(self):
        self.assertEqual(tokenizer.Tokenizer, type(self.dict_.create()))

    def test_get_part_of_speech_size(self):
        self.assertEqual(9, self.dict_.grammar.get_part_of_speech_size())

    def test_get_part_of_speech_string(self):
        pos = self.dict_.grammar.get_part_of_speech_string(0)
        self.assertIsNotNone(pos)
        self.assertEqual('助動詞', pos[0])

    # def test_creat_with_merging_settings

    # def test_creat_with_merging_null_ settings


if __name__ == '__main__':
    unittest.main()
