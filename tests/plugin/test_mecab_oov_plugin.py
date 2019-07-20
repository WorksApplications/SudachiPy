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
import tempfile
import unittest

from sudachipy.dictionarylib.categorytype import CategoryType
from sudachipy.plugin.oov import MeCabOovPlugin

from tests import mock_grammar, mock_inputtext


class TestMecabOOVPlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = MeCabOovPlugin()
        oov1 = MeCabOovPlugin.OOV()
        oov1.pos_id = 1
        oov2 = MeCabOovPlugin.OOV()
        oov2.pos_id = 2
        self.plugin.oov_list[CategoryType.KANJI] = [oov1]
        self.plugin.oov_list[CategoryType.KANJINUMERIC] = [oov1, oov2]
        self.mocked_input_text = mock_inputtext.mocked_input_text
        mock_inputtext.set_text('あいうえお')

        self.test_dir = tempfile.mkdtemp()

    def test_provide_oov000(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = False
        cinfo.is_group = False
        cinfo.length = 0
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(0, len(nodes))

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov100(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = True
        cinfo.is_group = False
        cinfo.length = 0
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(0, len(nodes))

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov010(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = False
        cinfo.is_group = True
        cinfo.length = 0
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(1, len(nodes))

        n = nodes[0]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov110(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = True
        cinfo.is_group = True
        cinfo.length = 0
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(1, len(nodes))

        n = nodes[0]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(1, len(nodes))

    def test_provide_oov002(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = False
        cinfo.is_group = False
        cinfo.length = 2
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(2, len(nodes))

        n = nodes[0]
        self.assertEqual('あ', n.get_word_info().surface)
        self.assertEqual(1, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[1]
        self.assertEqual('あい', n.get_word_info().surface)
        self.assertEqual(2, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov012(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = False
        cinfo.is_group = True
        cinfo.length = 2
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(3, len(nodes))

        n = nodes[0]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[1]
        self.assertEqual('あ', n.get_word_info().surface)
        self.assertEqual(1, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[2]
        self.assertEqual('あい', n.get_word_info().surface)
        self.assertEqual(2, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov112(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = True
        cinfo.is_group = True
        cinfo.length = 2
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(3, len(nodes))

        n = nodes[0]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[1]
        self.assertEqual('あ', n.get_word_info().surface)
        self.assertEqual(1, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[2]
        self.assertEqual('あい', n.get_word_info().surface)
        self.assertEqual(2, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(3, len(nodes))

    def test_provide_oov006(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJI
        cinfo.is_invoke = False
        cinfo.is_group = False
        cinfo.length = 6
        self.plugin.categories[CategoryType.KANJI] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(3, len(nodes))

        n = nodes[0]
        self.assertEqual('あ', n.get_word_info().surface)
        self.assertEqual(1, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[1]
        self.assertEqual('あい', n.get_word_info().surface)
        self.assertEqual(2, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[2]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, True)
        self.assertEqual(0, len(nodes))

    def test_provide_oov_multi_oov(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.KANJINUMERIC
        cinfo.is_invoke = False
        cinfo.is_group = True
        cinfo.length = 0
        self.plugin.categories[CategoryType.KANJINUMERIC] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.KANJINUMERIC)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(2, len(nodes))

        n = nodes[0]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(1, n.get_word_info().pos_id)

        n = nodes[1]
        self.assertEqual('あいう', n.get_word_info().surface)
        self.assertEqual(3, n.get_word_info().length())
        self.assertEqual(2, n.get_word_info().pos_id)

    def test_provide_oov_without_cinfo(self):
        mock_inputtext.set_category_type(0, 3, CategoryType.KANJI)
        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(0, len(nodes))

    def test_provide_oov_without_oov_list(self):
        cinfo = MeCabOovPlugin.CategoryInfo()
        cinfo.type_ = CategoryType.HIRAGANA
        cinfo.is_invoke = False
        cinfo.is_group = True
        cinfo.length = 0
        self.plugin.categories[CategoryType.HIRAGANA] = cinfo

        mock_inputtext.set_category_type(0, 3, CategoryType.HIRAGANA)

        nodes = self.plugin.provide_oov(self.mocked_input_text, 0, False)
        self.assertEqual(0, len(nodes))

    def test_read_character_property(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("#\n  \nDEFAULT 0 1 2\nALPHA 1 0 0\n0x0000...0x0002 ALPHA")
        plugin = MeCabOovPlugin()
        plugin.read_character_property(input_)
        self.assertFalse(plugin.categories[CategoryType.DEFAULT].is_invoke)
        self.assertTrue(plugin.categories[CategoryType.DEFAULT].is_group)
        self.assertEqual(2, plugin.categories[CategoryType.DEFAULT].length)

    def test_read_character_property_with_too_few_columns(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("DEFAULT 0 1\n")
        plugin = MeCabOovPlugin()
        with self.assertRaises(ValueError) as cm:
            plugin.read_character_property(input_)
        self.assertEqual('invalid format at line 1', cm.exception.args[0])

    def test_read_character_property_with_undefined_type(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("FOO 0 1 2\n")
        plugin = MeCabOovPlugin()
        with self.assertRaises(ValueError) as cm:
            plugin.read_character_property(input_)
        self.assertEqual('`FOO` is invalid type at line 1', cm.exception.args[0])

    def test_read_character_property_duplicate_definitions(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("DEFAULT 0 1 2\nDEFAULT 1 1 2")
        plugin = MeCabOovPlugin()
        with self.assertRaises(ValueError) as cm:
            plugin.read_character_property(input_)
        self.assertEqual('`DEFAULT` is already defined at line 2', cm.exception.args[0])

    def test_read_oov(self):
        oov = os.path.join(self.test_dir, 'test.txt')
        with open(oov, 'w') as wf:
            wf.write("DEFAULT,1,2,3,補助記号,一般,*,*,*,*\n")
            wf.write("DEFAULT,3,4,5,補助記号,一般,*,*,*,*\n")
        plugin = MeCabOovPlugin()
        plugin.categories[CategoryType.DEFAULT] = MeCabOovPlugin.CategoryInfo()
        plugin.read_oov(oov, mock_grammar.mocked_grammar)
        self.assertEqual(1, len(plugin.oov_list))
        self.assertEqual(2, len(plugin.oov_list[CategoryType.DEFAULT]))
        self.assertEqual(1, plugin.oov_list[CategoryType.DEFAULT][0].left_id)
        self.assertEqual(2, plugin.oov_list[CategoryType.DEFAULT][0].right_id)
        self.assertEqual(3, plugin.oov_list[CategoryType.DEFAULT][0].cost)
        self.assertEqual(0, plugin.oov_list[CategoryType.DEFAULT][0].pos_id)

    def test_read_oov_with_too_few_columns(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("DEFAULT,1,2,3\n")
        plugin = MeCabOovPlugin()
        plugin.categories[CategoryType.DEFAULT] = MeCabOovPlugin.CategoryInfo()
        with self.assertRaises(ValueError) as cm:
            plugin.read_oov(input_, mock_grammar.mocked_grammar)
        self.assertEqual('invalid format at line 1', cm.exception.args[0])

    def test_read_oov_with_undefined_type(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("FOO,1,2,3,補助記号,一般,*,*,*,*\n")
        plugin = MeCabOovPlugin()
        plugin.categories[CategoryType.DEFAULT] = MeCabOovPlugin.CategoryInfo()
        with self.assertRaises(ValueError) as cm:
            plugin.read_oov(input_, mock_grammar.mocked_grammar)
        self.assertEqual('`FOO` is invalid type at line 1', cm.exception.args[0])

    def test_read_oov_with_category_not_in_character_property(self):
        input_ = os.path.join(self.test_dir, 'test.txt')
        with open(input_, 'w') as wf:
            wf.write("ALPHA,1,2,3,補助記号,一般,*,*,*,*\n")
        plugin = MeCabOovPlugin()
        plugin.categories[CategoryType.DEFAULT] = MeCabOovPlugin.CategoryInfo()
        with self.assertRaises(ValueError) as cm:
            plugin.read_oov(input_, mock_grammar.mocked_grammar)
        self.assertEqual('`ALPHA` is undefined at line 1', cm.exception.args[0])


if __name__ == '__main__':
    unittest.main()
