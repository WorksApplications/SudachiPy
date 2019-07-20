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

from sudachipy.plugin.path_rewrite.numericparser import NumericParser


class TestNumericParser(TestCase):

    def setUp(self) -> None:
        self.parser = NumericParser()

    def test_digits(self):
        self.assertTrue(self.parse('1000'))
        self.assertEqual('1000', self.parser.get_normalized())
        self.parser.clear()

    def test_starts_with_zero(self):
        self.assertTrue(self.parse('001000'))
        self.assertEqual('001000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('〇一〇〇〇'))
        self.assertEqual('01000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('00.1000'))
        self.assertEqual('00.1', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('000'))
        self.assertEqual('000', self.parser.get_normalized())
        self.parser.clear()

    def test_use_small_unit(self):
        self.assertTrue(self.parse('二十七'))
        self.assertEqual('27', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千三百二十七'))
        self.assertEqual('1327', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千十七'))
        self.assertEqual('1017', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千三百二十七.〇五'))
        self.assertEqual('1327.05', self.parser.get_normalized())
        self.parser.clear()

        self.assertFalse(self.parse('三百二十百'))
        self.parser.clear()

    def test_use_large_unit(self):
        self.assertTrue(self.parse('1万'))
        self.assertEqual('10000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千三百二十七万'))
        self.assertEqual('13270000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千三百二十七万一四'))
        self.assertEqual('13270014', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('千三百二十七万一四.〇五'))
        self.assertEqual('13270014.05', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('三兆2千億千三百二十七万一四.〇五'))
        self.assertEqual('3200013270014.05', self.parser.get_normalized())
        self.parser.clear()

        self.assertFalse(self.parse('億万'))
        self.parser.clear()

    def test_float_with_unit(self):
        self.assertTrue(self.parse('1.5千'))
        self.assertEqual('1500', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('1.5百万'))
        self.assertEqual('1500000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('1.5百万1.5千20'))
        self.assertEqual('1501520', self.parser.get_normalized())
        self.parser.clear()

        self.assertFalse(self.parse('1.5千5百'))
        self.parser.clear()

        self.assertFalse(self.parse('1.5千500'))
        self.parser.clear()

    def test_log_numeric(self):
        self.assertTrue(self.parse('200000000000000000000万'))
        self.assertEqual('2000000000000000000000000', self.parser.get_normalized())
        self.parser.clear()

    def test_with_comma(self):
        self.assertTrue(self.parse('2,000,000'))
        self.assertEqual('2000000', self.parser.get_normalized())
        self.parser.clear()

        self.assertTrue(self.parse('259万2,300'))
        self.assertEqual('2592300', self.parser.get_normalized())
        self.parser.clear()

        self.assertFalse(self.parse('200,00,000'))
        self.assertEqual(NumericParser.Error.COMMA, self.parser._error_state)
        self.parser.clear()

        self.assertFalse(self.parse('2,4'))
        self.assertEqual(NumericParser.Error.COMMA, self.parser._error_state)
        self.parser.clear()

        self.assertFalse(self.parse('000,000'))
        self.assertEqual(NumericParser.Error.COMMA, self.parser._error_state)
        self.parser.clear()

        self.assertFalse(self.parse(',000'))
        self.assertEqual(NumericParser.Error.COMMA, self.parser._error_state)
        self.parser.clear()

        self.assertFalse(self.parse('256,55.1'))
        self.assertEqual(NumericParser.Error.COMMA, self.parser._error_state)
        self.parser.clear()

    def test_not_digit(self):
        self.assertFalse(self.parse('@@@'))
        self.parser.clear()

    def test_float_point(self):
        self.assertTrue(self.parse('6.0'))
        self.assertEqual('6', self.parser.get_normalized())
        self.parser.clear()

        self.assertFalse(self.parse('6.'))
        self.assertEqual(NumericParser.Error.POINT, self.parser.error_state)
        self.parser.clear()

        self.assertFalse(self.parse('1.2.3'))
        self.assertEqual(NumericParser.Error.POINT, self.parser.error_state)
        self.parser.clear()

    def parse(self, text: str) -> bool:
        for c in text:
            if not self.parser.append(c):
                return False
        return self.parser.done()
