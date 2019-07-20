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

from unittest import TestCase

from sudachipy.plugin.input_text import ProlongedSoundMarkInputTextPlugin
from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder

from tests.mock_grammar import mocked_grammar


class TestProlongedSoundMarkInputTextPlugin(TestCase):

    def setUp(self) -> None:
        self.plugin = ProlongedSoundMarkInputTextPlugin(None)
        for psm in ['ー', '〜', '〰']:
            self.plugin._psm_set.add(ord(psm))

    def test_combine_continuous_prolonged_sound_mark(self):
        original = 'ゴーール'
        normalized = 'ゴール'
        builder = UTF8InputTextBuilder(original, mocked_grammar)
        self.plugin.rewrite(builder)
        text = builder.build()

        self.assertEqual(original, text.original_text)
        self.assertEqual(normalized, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(9, len(bytes_))

        self.assertEqual(b'\xe3\x82\xb4\xe3\x83\xbc\xe3\x83\xab', bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(1, text.get_original_index(3))
        self.assertEqual(3, text.get_original_index(6))
        self.assertEqual(4, text.get_original_index(9))

    def test_combined_continuous_prolonged_sound_marks_at_end(self):
        original = 'スーパーー'
        normalized = 'スーパー'
        builder = UTF8InputTextBuilder(original, mocked_grammar)
        self.plugin.rewrite(builder)
        text = builder.build()

        self.assertEqual(original, text.original_text)
        self.assertEqual(normalized, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(12, len(bytes_))

        self.assertEqual(b'\xe3\x82\xb9\xe3\x83\xbc\xe3\x83\x91\xe3\x83\xbc', bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(1, text.get_original_index(3))
        self.assertEqual(2, text.get_original_index(6))
        self.assertEqual(3, text.get_original_index(9))
        self.assertEqual(5, text.get_original_index(12))

    def test_combine_continuous_prolonged_sound_marks_multi_times(self):
        original = 'エーービーーーシーーーー'
        normalized = 'エービーシー'
        builder = UTF8InputTextBuilder(original, mocked_grammar)
        self.plugin.rewrite(builder)
        text = builder.build()

        self.assertEqual(original, text.original_text)
        self.assertEqual(normalized, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(18, len(bytes_))

        self.assertEqual(b'\xe3\x82\xa8\xe3\x83\xbc\xe3\x83\x93\xe3\x83\xbc\xe3\x82\xb7\xe3\x83\xbc', bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(1, text.get_original_index(3))
        self.assertEqual(3, text.get_original_index(6))
        self.assertEqual(4, text.get_original_index(9))
        self.assertEqual(7, text.get_original_index(12))
        self.assertEqual(8, text.get_original_index(15))
        self.assertEqual(12, text.get_original_index(18))

    def test_combine_continuous_prolonged_sound_marks_multi_symbol_types(self):
        original = 'エーービ〜〜〜シ〰〰〰〰'
        normalized = 'エービーシー'
        builder = UTF8InputTextBuilder(original, mocked_grammar)
        self.plugin.rewrite(builder)
        text = builder.build()

        self.assertEqual(original, text.original_text)
        self.assertEqual(normalized, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(18, len(bytes_))

        self.assertEqual(b'\xe3\x82\xa8\xe3\x83\xbc\xe3\x83\x93\xe3\x83\xbc\xe3\x82\xb7\xe3\x83\xbc', bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(1, text.get_original_index(3))
        self.assertEqual(3, text.get_original_index(6))
        self.assertEqual(4, text.get_original_index(9))
        self.assertEqual(7, text.get_original_index(12))
        self.assertEqual(8, text.get_original_index(15))
        self.assertEqual(12, text.get_original_index(18))

    def test_combine_continuous_prolonged_sound_marks_multi_mixed_symbol_types(self):
        original = 'エー〜ビ〜〰ーシ〰ー〰〜'
        normalized = 'エービーシー'
        builder = UTF8InputTextBuilder(original, mocked_grammar)
        self.plugin.rewrite(builder)
        text = builder.build()

        self.assertEqual(original, text.original_text)
        self.assertEqual(normalized, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(18, len(bytes_))

        self.assertEqual(b'\xe3\x82\xa8\xe3\x83\xbc\xe3\x83\x93\xe3\x83\xbc\xe3\x82\xb7\xe3\x83\xbc', bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(1, text.get_original_index(3))
        self.assertEqual(3, text.get_original_index(6))
        self.assertEqual(4, text.get_original_index(9))
        self.assertEqual(7, text.get_original_index(12))
        self.assertEqual(8, text.get_original_index(15))
        self.assertEqual(12, text.get_original_index(18))
