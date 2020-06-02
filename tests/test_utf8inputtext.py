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

import sudachipy
import sudachipy.dictionarylib as dictionarylib


class TestUTF8InputText(unittest.TestCase):

    def setUp(self):
        self.TEXT = "âｂC1あ234漢字𡈽アｺﾞ"
        self.bytes = [
            b'0xC3', b'0xA2', b'0xEF', b'0xBD', b'0x82',
            b'0x43', b'0x31', b'0xE3', b'0x81', b'0x82',
            b'0x32', b'0x33', b'0x34', b'0xE6', b'0xBC',
            b'0xA2', b'0xE5', b'0xAD', b'0x97', b'0xF0',
            b'0xA1', b'0x88', b'0xBD', b'0xE3', b'0x82',
            b'0xA2', b'0xEF', b'0xBD', b'0xBA', b'0xEF',
            b'0xBE', b'0x9E'
        ]

        self.input = None

        grammar = self.MockGrammar()
        char_category = dictionarylib.charactercategory.CharacterCategory()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        char_category.read_character_definition(os.path.join(this_dir, 'resources/char.def'))
        grammar.set_character_category(char_category)

        self.builder = sudachipy.utf8inputtextbuilder.UTF8InputTextBuilder(self.TEXT, grammar)

    def test_get_original_text(self):
        self.assertEqual(self.builder.get_original_text(), self.TEXT)
        self.assertEqual(self.builder.get_text(), self.TEXT)
        self.input = self.builder.build()
        self.assertEqual(self.input.get_original_text(), self.TEXT)
        self.assertEqual(self.input.get_text(), self.TEXT)

    def test_get_byte_text(self):
        input_ = self.builder.build()
        self.assertEqual(len(input_.get_byte_text()), 32)
        self.assertEqual(self.TEXT.encode('utf-8'), input_.get_byte_text())

    def test_get_original_index(self):
        input_ = self.builder.build()
        self.assertEqual(input_.get_original_index(0), 0)
        self.assertEqual(input_.get_original_index(1), 0)
        self.assertEqual(input_.get_original_index(2), 1)
        self.assertEqual(input_.get_original_index(4), 1)
        self.assertEqual(input_.get_original_index(6), 3)
        self.assertEqual(input_.get_original_index(7), 4)
        self.assertEqual(input_.get_original_index(10), 5)
        self.assertEqual(input_.get_original_index(18), 9)
        self.assertEqual(input_.get_original_index(19), 10)
        self.assertEqual(input_.get_original_index(22), 10)
        self.assertEqual(input_.get_original_index(23), 11)
        self.assertEqual(input_.get_original_index(28), 12)
        self.assertEqual(input_.get_original_index(31), 13)

    def test_get_char_category_types(self):
        input_ = self.builder.build()
        self.assertTrue(dictionarylib.categorytype.CategoryType.ALPHA in input_.get_char_category_types(0))
        self.assertTrue(dictionarylib.categorytype.CategoryType.ALPHA in input_.get_char_category_types(2))
        self.assertTrue(dictionarylib.categorytype.CategoryType.ALPHA in input_.get_char_category_types(5))
        self.assertTrue(dictionarylib.categorytype.CategoryType.NUMERIC in input_.get_char_category_types(6))
        self.assertTrue(dictionarylib.categorytype.CategoryType.HIRAGANA in input_.get_char_category_types(7))
        self.assertTrue(dictionarylib.categorytype.CategoryType.HIRAGANA in input_.get_char_category_types(9))
        self.assertTrue(dictionarylib.categorytype.CategoryType.NUMERIC in input_.get_char_category_types(10))
        self.assertTrue(dictionarylib.categorytype.CategoryType.KANJI in input_.get_char_category_types(13))
        self.assertTrue(dictionarylib.categorytype.CategoryType.KANJI in input_.get_char_category_types(18))
        self.assertTrue(dictionarylib.categorytype.CategoryType.DEFAULT in input_.get_char_category_types(19))
        self.assertTrue(dictionarylib.categorytype.CategoryType.DEFAULT in input_.get_char_category_types(22))
        self.assertTrue(dictionarylib.categorytype.CategoryType.KATAKANA in input_.get_char_category_types(23))
        self.assertTrue(dictionarylib.categorytype.CategoryType.KATAKANA in input_.get_char_category_types(26))
        self.assertTrue(dictionarylib.categorytype.CategoryType.KATAKANA in input_.get_char_category_types(31))

    def test_get_char_category_continuous_length(self):
        input_ = self.builder.build()
        self.assertEqual(input_.get_char_category_continuous_length(0), 6)
        self.assertEqual(input_.get_char_category_continuous_length(1), 5)
        self.assertEqual(input_.get_char_category_continuous_length(2), 4)
        self.assertEqual(input_.get_char_category_continuous_length(5), 1)
        self.assertEqual(input_.get_char_category_continuous_length(6), 1)
        self.assertEqual(input_.get_char_category_continuous_length(7), 3)
        self.assertEqual(input_.get_char_category_continuous_length(10), 3)
        self.assertEqual(input_.get_char_category_continuous_length(11), 2)
        self.assertEqual(input_.get_char_category_continuous_length(12), 1)
        self.assertEqual(input_.get_char_category_continuous_length(19), 4)
        self.assertEqual(input_.get_char_category_continuous_length(22), 1)
        self.assertEqual(input_.get_char_category_continuous_length(23), 9)
        self.assertEqual(input_.get_char_category_continuous_length(26), 6)
        self.assertEqual(input_.get_char_category_continuous_length(31), 1)

    def test_replace_with_same_length(self):
        self.builder.replace(8, 10, "ああ")
        self.assertEqual(self.builder.get_original_text(), self.TEXT)
        self.assertEqual(self.builder.get_text(), "âｂC1あ234ああ𡈽アｺﾞ")
        input_ = self.builder.build()
        self.assertEqual(input_.get_original_text(), self.TEXT)
        self.assertEqual(input_.get_text(), "âｂC1あ234ああ𡈽アｺﾞ")
        self.assertEqual(len(input_.get_byte_text()), 32)
        self.assertEqual(input_.get_original_index(0), 0)
        self.assertEqual(input_.get_original_index(12), 7)
        self.assertEqual(input_.get_original_index(13), 8)
        self.assertEqual(input_.get_original_index(15), 8)
        self.assertEqual(input_.get_original_index(16), 10)
        self.assertEqual(input_.get_original_index(18), 10)
        self.assertEqual(input_.get_original_index(19), 10)
        self.assertEqual(input_.get_original_index(22), 10)
        self.assertEqual(input_.get_original_index(31), 13)

    def test_replaceWithDeletion(self):
        self.builder.replace(8, 10, "あ")
        self.assertEqual(self.builder.get_original_text(), self.TEXT)
        self.assertEqual(self.builder.get_text(), "âｂC1あ234あ𡈽アｺﾞ")
        input_ = self.builder.build()
        self.assertEqual(input_.get_original_text(), self.TEXT)
        self.assertEqual(input_.get_text(), "âｂC1あ234あ𡈽アｺﾞ")
        self.assertEqual(len(input_.get_byte_text()), 29)
        self.assertEqual(input_.get_original_index(0), 0)
        self.assertEqual(input_.get_original_index(12), 7)
        self.assertEqual(input_.get_original_index(13), 8)
        self.assertEqual(input_.get_original_index(15), 8)
        self.assertEqual(input_.get_original_index(16), 10)
        self.assertEqual(input_.get_original_index(19), 10)
        self.assertEqual(input_.get_original_index(28), 13)

    def test_replaceWithInsertion(self):
        self.builder.replace(8, 10, "あああ")
        self.assertEqual(self.builder.get_original_text(), self.TEXT)
        self.assertEqual(self.builder.get_text(), "âｂC1あ234あああ𡈽アｺﾞ")
        input_ = self.builder.build()
        self.assertEqual(input_.get_original_text(), self.TEXT)
        self.assertEqual(input_.get_text(), "âｂC1あ234あああ𡈽アｺﾞ")
        self.assertEqual(len(input_.get_byte_text()), 35)
        self.assertEqual(input_.get_original_index(0), 0)  # â
        self.assertEqual(input_.get_original_index(12), 7)  # 4
        self.assertEqual(input_.get_original_index(13), 8)  # >あ< ああ
        self.assertEqual(input_.get_original_index(21), 10)  # ああ >あ<
        self.assertEqual(input_.get_original_index(22), 10)  # 𡈽
        self.assertEqual(input_.get_original_index(25), 10)  # 𡈽
        self.assertEqual(input_.get_original_index(35), 14)  #  ﾞ

    def test_replaceMultiTimes(self):
        self.builder.replace(0, 1, "a")
        self.builder.replace(1, 2, "b")
        self.builder.replace(2, 3, "c")
        self.builder.replace(10, 11, "土")
        self.builder.replace(12, 14, "ゴ")
        input_ = self.builder.build()
        self.assertEqual(input_.get_original_text(), self.TEXT)
        self.assertEqual(input_.get_text(), "abc1あ234漢字土アゴ")
        self.assertEqual(len(input_.get_byte_text()), 25)
        self.assertEqual(input_.get_original_index(0), 0)
        self.assertEqual(input_.get_original_index(1), 1)
        self.assertEqual(input_.get_original_index(2), 2)
        self.assertEqual(input_.get_original_index(7), 5)
        self.assertEqual(input_.get_original_index(8), 6)
        self.assertEqual(input_.get_original_index(9), 7)
        self.assertEqual(input_.get_original_index(15), 9)
        self.assertEqual(input_.get_original_index(16), 10)
        self.assertEqual(input_.get_original_index(18), 10)
        self.assertEqual(input_.get_original_index(19), 11)
        self.assertEqual(input_.get_original_index(21), 11)
        self.assertEqual(input_.get_original_index(22), 12)
        self.assertEqual(input_.get_original_index(24), 12)

    def test_getByteLengthByCodePoints(self):
        input_ = self.builder.build()
        self.assertEqual(input_.get_code_points_offset_length(0, 1), 2)
        self.assertEqual(input_.get_code_points_offset_length(0, 4), 7)
        self.assertEqual(input_.get_code_points_offset_length(10, 1), 1)
        self.assertEqual(input_.get_code_points_offset_length(11, 1), 1)
        self.assertEqual(input_.get_code_points_offset_length(12, 1), 1)
        self.assertEqual(input_.get_code_points_offset_length(13, 2), 6)
        self.assertEqual(input_.get_code_points_offset_length(19, 1), 4)
        self.assertEqual(input_.get_code_points_offset_length(23, 3), 9)

    def test_codePointCount(self):
        input_ = self.builder.build()
        self.assertEqual(input_.code_point_count(0, 2), 1)
        self.assertEqual(input_.code_point_count(0, 7), 4)
        self.assertEqual(input_.code_point_count(13, 19), 2)

    def test_canBow(self):
        input_ = self.builder.build()
        self.assertTrue(input_.can_bow(0))  # â
        self.assertFalse(input_.can_bow(1))
        self.assertFalse(input_.can_bow(2))  # ｂ
        self.assertFalse(input_.can_bow(3))
        self.assertFalse(input_.can_bow(4))
        self.assertFalse(input_.can_bow(5))  # C
        self.assertTrue(input_.can_bow(6))  # 1
        self.assertTrue(input_.can_bow(7))  # あ

        self.assertTrue(input_.can_bow(19))  # 𡈽
        self.assertFalse(input_.can_bow(20))
        self.assertFalse(input_.can_bow(21))
        self.assertFalse(input_.can_bow(22))
        self.assertTrue(input_.can_bow(23))  # ア

    def test_getWordCandidateLength(self):
        input_ = self.builder.build()
        self.assertEqual(input_.get_word_candidate_length(0), 6)
        self.assertEqual(input_.get_word_candidate_length(6), 1)
        self.assertEqual(input_.get_word_candidate_length(19), 4)
        self.assertEqual(input_.get_word_candidate_length(29), 3)

    class MockGrammar:
        char_category = None

        def get_part_of_speech_size(self):
            return 0

        def get_part_of_speech_string(self, pos_id):
            return None

        def get_part_of_speech_id(self, pos):
            return 0

        def get_connect_cost(self, left_id, right_id, cost=None):
            if cost is None:
                return 0
            else:
                return

        def get_bos_parameter(self):
            return None

        def get_eos_parameter(self):
            return None

        def get_character_category(self):
            return self.char_category

        def set_character_category(self, char_category):
            self.char_category = char_category


if __name__ == '__main__':
    unittest.main()
