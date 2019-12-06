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
from sudachipy.dictionarylib.doublearraylexicon import DoubleArrayLexicon


class TestDoubleArrayLexicon(unittest.TestCase):

    __GRAMMAR_SIZE = 470

    def setUp(self):
        # Copied from sudachipy.dictionay.Dictionary.read_system_dictionary
        test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')
        filename = os.path.join(test_resources_dir, 'system.dic')
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        header = DictionaryHeader.from_bytes(bytes_, 0)
        if header.version != SYSTEM_DICT_VERSION:
            raise Exception('invalid system dictionary')
        self.lexicon = DoubleArrayLexicon(bytes_, header.storage_size() + 470)

    def test_lookup(self):
        res = self.lexicon.lookup('東京都'.encode('utf-8'), 0)
        self.assertEqual((4, 3), res.__next__())  # 東

        self.assertEqual((5, 6), res.__next__())  # 東京

        self.assertEqual((6, 9), res.__next__())  # 東京都

        with self.assertRaises(StopIteration):
            res.__next__()

        res = self.lexicon.lookup('東京都に'.encode('utf-8'), 9)
        self.assertEqual((1, 12), res.__next__())  # に(接続助詞)
        self.assertEqual((2, 12), res.__next__())  # に(格助詞)
        with self.assertRaises(StopIteration):
            res.__next__()

        res = self.lexicon.lookup('あれ'.encode('utf-8'), 0)
        with self.assertRaises(StopIteration):
            res.__next__()

    def test_parameters(self):
        # た
        self.assertEqual(1, self.lexicon.get_left_id(0))
        self.assertEqual(1, self.lexicon.get_right_id(0))
        self.assertEqual(8729, self.lexicon.get_cost(0))

        # 東京都
        self.assertEqual(6, self.lexicon.get_left_id(6))
        self.assertEqual(8, self.lexicon.get_right_id(6))
        self.assertEqual(5320, self.lexicon.get_cost(6))

        # 都
        self.assertEqual(8, self.lexicon.get_left_id(9))
        self.assertEqual(8, self.lexicon.get_right_id(9))
        self.assertEqual(2914, self.lexicon.get_cost(9))

    def test_wordinfo(self):
        # た
        wi = self.lexicon.get_word_info(0)
        self.assertEqual('た', wi.surface)
        self.assertEqual(3, wi.head_word_length)
        self.assertEqual(0, wi.pos_id)
        self.assertEqual('た', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('た', wi.dictionary_form)
        self.assertEqual('タ', wi.reading_form)
        self.assertEqual([], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        self.assertEqual([], wi.word_structure)

        # 行っ
        wi = self.lexicon.get_word_info(8)
        self.assertEqual('行っ', wi.surface)
        self.assertEqual('行く', wi.normalized_form)
        self.assertEqual(7, wi.dictionary_form_word_id)
        self.assertEqual('行く', wi.dictionary_form)

        # 東京都
        wi = self.lexicon.get_word_info(6)
        self.assertEqual('東京都', wi.surface)
        self.assertEqual([5, 9], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        self.assertEqual([5, 9], wi.word_structure)

    def test_wordinfo_with_longword(self):
        # 0123456789 * 30
        wi = self.lexicon.get_word_info(36)
        self.assertEqual(300, len(wi.surface))
        self.assertEqual(300, wi.head_word_length)
        self.assertEqual(300, len(wi.normalized_form))
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual(300, len(wi.dictionary_form))
        self.assertEqual(570, len(wi.reading_form))

    def test_size(self):
        self.assertEqual(38, self.lexicon.size())


if __name__ == '__main__':
    unittest.main()
