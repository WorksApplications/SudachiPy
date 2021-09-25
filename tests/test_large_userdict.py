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

from string import ascii_lowercase
from itertools import product

from sudachipy import dictionary


class TestLargeUserDict(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.dict_ = dictionary.Dictionary(os.path.join(resource_dir, 'sudachi_large_user.json'), resource_dir)
        self.tokenizer_obj = self.dict_.create()

    def test_part_of_speech(self):
        ms = self.tokenizer_obj.tokenize('やまもも')
        self.assertEqual(1, len(ms))
        m = ms[0]
        pid = m.part_of_speech_id()
        self.assertTrue(self.dict_.grammar.get_part_of_speech_size() > pid)

        # Exploit the cache space
        num = 0
        for combo in product(ascii_lowercase, repeat=3):
            if num > 1024:
                break
            lex = ''.join(combo)
            self.tokenizer_obj.tokenize(lex)
            num += 1

        ms = self.tokenizer_obj.tokenize('やまもも')
        self.assertEqual(pid, ms[0].part_of_speech_id())
