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

from sudachipy.plugin.input_text.default_input_text_plugin import DefaultInputTextPlugin
from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder

from tests import mock_grammar


class TestDefaultInputTextPlugin(unittest.TestCase):

    original_text = "ÂＢΓД㈱ｶﾞウ゛⼼Ⅲ"
    normalized_text = "âbγд(株)ガヴ⼼ⅲ"

    def setUp(self):
        self.builder = UTF8InputTextBuilder(self.original_text, mock_grammar.mocked_grammar)

        self.plugin = DefaultInputTextPlugin()

        try:
            self.plugin.set_up()
        except IOError:
            self.fail('no file')

        self.test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')

    def test_before_rewrite(self):
        self.assertEqual(self.original_text, self.builder.get_original_text())
        self.assertEqual(self.original_text, self.builder.get_text())
        text = self.builder.build()
        self.assertEqual(self.original_text, text.get_original_text())
        self.assertEqual(self.original_text, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(30, len(bytes_))
        expected = b'\xc3\x82\xef\xbc\xa2\xce\x93\xd0\x94\xe3\x88\xb1\xef\xbd\xb6\xef\xbe\x9e\xe3\x82\xa6\xe3\x82\x9b\xe2\xbc\xbc\xe2\x85\xa2'
        self.assertEqual(expected, bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(0, text.get_original_index(1))
        self.assertEqual(1, text.get_original_index(2))
        self.assertEqual(1, text.get_original_index(4))
        self.assertEqual(3, text.get_original_index(8))
        self.assertEqual(5, text.get_original_index(12))
        self.assertEqual(9, text.get_original_index(24))
        self.assertEqual(9, text.get_original_index(26))

    def test_after_rewrite(self):
        self.assertEqual(self.original_text, self.builder.get_original_text())
        self.assertEqual(self.original_text, self.builder.get_text())
        self.plugin.rewrite(self.builder)
        text = self.builder.build()
        self.assertEqual(self.original_text, text.get_original_text())
        self.assertEqual(self.normalized_text, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(24, len(bytes_))
        expected = b'\xc3\xa2\x62\xce\xb3\xd0\xb4\x28\xe6\xa0\xaa\x29\xe3\x82\xac\xe3\x83\xb4\xe2\xbc\xbc\xe2\x85\xb2'
        self.assertEqual(expected, bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(0, text.get_original_index(1))
        self.assertEqual(1, text.get_original_index(2))
        self.assertEqual(2, text.get_original_index(3))
        self.assertEqual(4, text.get_original_index(7))
        self.assertEqual(5, text.get_original_index(8))
        self.assertEqual(5, text.get_original_index(11))
        self.assertEqual(7, text.get_original_index(15))
        self.assertEqual(7, text.get_original_index(17))

    # def test_setup_with_null(self):

    def test_invalid_format_ignorelist(self):
        plugin = DefaultInputTextPlugin()
        with self.assertRaises(RuntimeError) as cm:
            plugin.read_rewrite_lists(os.path.join(self.test_resources_dir, 'rewrite_error_ignorelist.def'))
        self.assertEqual('12 is not character at line 1', cm.exception.args[0])

    def test_invalid_format_replacelist(self):
        plugin = DefaultInputTextPlugin()
        with self.assertRaises(RuntimeError) as cm:
            plugin.read_rewrite_lists(os.path.join(self.test_resources_dir, 'rewrite_error_replacelist.def'))
        self.assertEqual('invalid format at line 1', cm.exception.args[0])

    def test_duplicated_lines_replacelist(self):
        plugin = DefaultInputTextPlugin()
        with self.assertRaises(RuntimeError) as cm:
            plugin.read_rewrite_lists(os.path.join(self.test_resources_dir, 'rewrite_error_dup.def'))
        self.assertEqual('12 is already defined at line 2', cm.exception.args[0])


if __name__ == '__main__':
    unittest.main()
