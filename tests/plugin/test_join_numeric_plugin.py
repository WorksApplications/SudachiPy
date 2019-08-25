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

from sudachipy.dictionary import Dictionary
from sudachipy.plugin.path_rewrite import JoinNumericPlugin
from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder


class TestJoinNumericOOVPlugin(unittest.TestCase):

    def setUp(self):
        pass
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources')
        self.dict_ = Dictionary(os.path.join(resource_dir, 'numeric_sudachi.json'), resource_dir)
        self.tokenizer = self.dict_.create()
        self.plugin = JoinNumericPlugin(None)
        self.plugin.set_up(self.dict_.grammar)

    def test_digit(self):
        path = self.get_path('123円20銭')
        self.assertEqual(4, len(path))
        self.assertEqual('123', path[0].get_word_info().surface)
        self.assertEqual('20', path[2].get_word_info().surface)

        path = self.get_path('080-121')
        self.assertEqual(3, len(path))
        self.assertEqual('080', path[0].get_word_info().surface)
        self.assertEqual('121', path[2].get_word_info().surface)

    def test_kanji_numeric(self):
        path = self.get_path('一二三万二千円')
        self.assertEqual(2, len(path))
        self.assertEqual('一二三万二千', path[0].get_word_info().surface)

        path = self.get_path('二百百')
        self.assertEqual(3, len(path))

    def test_normalize(self):
        self.plugin._enable_normalize = True
        path = self.get_path('一二三万二千円')
        self.assertEqual(2, len(path))
        self.assertEqual('1232000', path[0].get_word_info().normalized_form)

    def test_normalized_with_not_numeric(self):
        self.plugin._enable_normalize = True
        path = self.get_path('六三四')
        self.assertEqual(1, len(path))
        self.assertEqual('六三四', path[0].get_word_info().normalized_form)

    def test_point(self):
        self.plugin._enable_normalize = True

        path = self.get_path('1.002')
        self.assertEqual(1, len(path))
        self.assertEqual('1.002', path[0].get_word_info().normalized_form)

        path = self.get_path('.002')
        self.assertEqual(2, len(path))
        self.assertEqual('.', path[0].get_word_info().normalized_form)
        self.assertEqual('002', path[1].get_word_info().normalized_form)

        path = self.get_path('22.')
        self.assertEqual(2, len(path))
        self.assertEqual('22', path[0].get_word_info().normalized_form)
        self.assertEqual('.', path[1].get_word_info().normalized_form)

        path = self.get_path('22.節')
        self.assertEqual(3, len(path))
        self.assertEqual('22', path[0].get_word_info().normalized_form)
        self.assertEqual('.', path[1].get_word_info().normalized_form)

        path = self.get_path('.c')
        self.assertEqual(2, len(path))
        self.assertEqual('.', path[0].get_word_info().normalized_form)

        path = self.get_path('1.20.3')
        self.assertEqual(5, len(path))
        self.assertEqual('20', path[2].get_word_info().normalized_form)

        path = self.get_path('652...')
        self.assertEqual(4, len(path))
        self.assertEqual('652', path[0].get_word_info().normalized_form)

    def test_comma(self):
        self.plugin._enable_normalize = True

        path = self.get_path('2,000,000')
        self.assertEqual(1, len(path))
        self.assertEqual('2000000', path[0].get_word_info().normalized_form)

        path = self.get_path('2,00,000,000円')
        self.assertEqual(8, len(path))
        self.assertEqual('2', path[0].get_word_info().normalized_form)
        self.assertEqual(',', path[1].get_word_info().normalized_form)
        self.assertEqual('00', path[2].get_word_info().normalized_form)
        self.assertEqual(',', path[3].get_word_info().normalized_form)
        self.assertEqual('000', path[4].get_word_info().normalized_form)
        self.assertEqual(',', path[5].get_word_info().normalized_form)
        self.assertEqual('000', path[6].get_word_info().normalized_form)

        path = self.get_path(',')
        self.assertEqual(1, len(path))

        path = self.get_path('652,,,')
        self.assertEqual(4, len(path))
        self.assertEqual('652', path[0].get_word_info().normalized_form)

        path = self.get_path('256,5.50389')
        self.assertEqual(3, len(path))
        self.assertEqual('256', path[0].get_word_info().normalized_form)
        self.assertEqual('5.50389', path[2].get_word_info().normalized_form)

        path = self.get_path('256,550.389')
        self.assertEqual(1, len(path))
        self.assertEqual('256550.389', path[0].get_word_info().normalized_form)

    def test_single_node(self):
        self.plugin._enable_normalize = False
        path = self.get_path('猫三匹')
        self.assertEqual(3, len(path))
        self.assertEqual('三', path[1].get_word_info().normalized_form)

        self.plugin._enable_normalize = True
        path = self.get_path('猫三匹')
        self.assertEqual(3, len(path))
        self.assertEqual('3', path[1].get_word_info().normalized_form)

    def get_path(self, text: str):
        input_ = UTF8InputTextBuilder(text, self.tokenizer._grammar).build()
        self.tokenizer._build_lattice(input_)
        path = self.tokenizer._lattice.get_best_path()
        self.plugin.rewrite(input_, path, self.tokenizer._lattice)
        self.tokenizer._lattice.clear()
        return path


if __name__ == '__main__':
    unittest.main()
