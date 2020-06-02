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

from sudachipy import dictionary


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.dict_ = dictionary.Dictionary(os.path.join(resource_dir, 'sudachi.json'), resource_dir)
        self.tokenizer_obj = self.dict_.create()

    def test_tokenize_small_katanana_only(self):
        ms = self.tokenizer_obj.tokenize('ァ')
        self.assertEqual(1, len(ms))

    def test_part_of_speech(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, len(ms))
        m = ms[0]
        pid = m.part_of_speech_id()
        self.assertTrue(self.dict_.grammar.get_part_of_speech_size() > pid)
        pos = m.part_of_speech()
        self.assertEqual(pos, self.dict_.grammar.get_part_of_speech_string(pid))

    def test_get_word_id(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, len(ms))
        self.assertEqual(['名詞', '固有名詞', '地名', '一般', '*', '*'], ms[0].part_of_speech())

        wid = ms[0].word_id()
        ms = self.tokenizer_obj.tokenize('ぴらる')
        self.assertEqual(1, len(ms))
        self.assertNotEqual(wid, ms[0].word_id())
        self.assertEqual(['名詞', '普通名詞', '一般', '*', '*', '*'], ms[0].part_of_speech())

        ms = self.tokenizer_obj.tokenize('京')
        self.assertEqual(1, len(ms))

    def test_get_dictionary_id(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, ms.size())
        self.assertEqual(0, ms[0].dictionary_id())

        ms = self.tokenizer_obj.tokenize('ぴらる')
        self.assertEqual(1, ms.size())
        self.assertEqual(1, ms[0].dictionary_id())

        ms = self.tokenizer_obj.tokenize('京')
        self.assertEqual(1, ms.size())
        self.assertTrue(ms[0].dictionary_id() < 0)

    def test_tokenize_kanji_alphabet_word(self):
        self.assertEqual(len(self.tokenizer_obj.tokenize('特a')), 1)
        self.assertEqual(len(self.tokenizer_obj.tokenize('ab')), 1)
        self.assertEqual(len(self.tokenizer_obj.tokenize('特ab')), 2)

    def test_tokenizer_with_dots(self):
        ms = self.tokenizer_obj.tokenize('京都…')
        self.assertEqual(4, ms.size())
        self.assertEqual(ms[1].surface(), '…')
        self.assertEqual(ms[1].normalized_form(), '.')
        self.assertEqual(ms[2].surface(), '')
        self.assertEqual(ms[2].normalized_form(), '.')
        self.assertEqual(ms[3].surface(), '')
        self.assertEqual(ms[3].normalized_form(), '.')


if __name__ == '__main__':
    unittest.main()
