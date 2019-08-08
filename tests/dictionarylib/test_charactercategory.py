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
import shutil
import tempfile
import unittest

from sudachipy.dictionarylib import charactercategory
from sudachipy.dictionarylib.categorytype import CategoryType


class TestCharacterCategory(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')
        pass

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_range_containing_length(self):
        range_ = charactercategory.CharacterCategory.Range()
        range_.low = 0x41
        range_.high = 0x54
        self.assertEqual(3, range_.containing_length('ABC12'))
        self.assertEqual(0, range_.containing_length('熙'))

    def test_get_category_types(self):
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(os.path.join(self.test_resources_dir, 'char.def'))
        self.assertEqual({CategoryType.KANJI}, cat.get_category_types(ord('熙')))
        self.assertNotEqual({CategoryType.DEFAULT}, cat.get_category_types(ord('熙')))

    def test_read_character_definition(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("#\n \n")
            wf.write("0x0030..0x0039 NUMERIC\n")
            wf.write("0x0032         KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({CategoryType.NUMERIC}, cat.get_category_types(0x0030))
        self.assertEqual({CategoryType.NUMERIC}, cat.get_category_types(0x0031))
        self.assertEqual({CategoryType.NUMERIC, CategoryType.KANJI}, cat.get_category_types(0x0032))
        self.assertEqual({CategoryType.NUMERIC}, cat.get_category_types(0x0033))
        self.assertEqual({CategoryType.NUMERIC}, cat.get_category_types(0x0039))

        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("#\n \n")
            wf.write("0x0030..0x0039 NUMERIC\n")
            wf.write("0x0070..0x0079 ALPHA\n")
            wf.write("0x3007         KANJI\n")
            wf.write("0x0030         KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({CategoryType.NUMERIC, CategoryType.KANJI}, cat.get_category_types(0x0030))
        self.assertEqual({CategoryType.NUMERIC}, cat.get_category_types(0x0039))
        self.assertEqual({CategoryType.KANJI}, cat.get_category_types(0x3007))
        self.assertEqual({CategoryType.DEFAULT}, cat.get_category_types(0x0069))
        self.assertEqual({CategoryType.ALPHA}, cat.get_category_types(0x0070))
        self.assertEqual({CategoryType.DEFAULT}, cat.get_category_types(0x0080))

        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("#\n \n")
            wf.write("0x0030..0x0039 KATAKANA\n")
            wf.write("0x3007         KANJI KANJINUMERIC\n")
            wf.write("0x3008         KANJI KANJINUMERIC\n")
            wf.write("0x3009         KANJI KANJINUMERIC\n")
            wf.write("0x0039..0x0040 ALPHA\n")
            wf.write("0x0030..0x0039 NUMERIC\n")
            wf.write("0x0030         KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({CategoryType.DEFAULT}, cat.get_category_types(0x0029))
        self.assertEqual({CategoryType.NUMERIC, CategoryType.KANJI, CategoryType.KATAKANA}, cat.get_category_types(0x0030))
        self.assertEqual({CategoryType.NUMERIC, CategoryType.KATAKANA, CategoryType.ALPHA}, cat.get_category_types(0x0039))
        self.assertEqual({CategoryType.ALPHA}, cat.get_category_types(0x0040))
        self.assertEqual({CategoryType.DEFAULT}, cat.get_category_types(0x0041))
        self.assertEqual({CategoryType.KANJI, CategoryType.KANJINUMERIC}, cat.get_category_types(0x3007))
        self.assertEqual({CategoryType.DEFAULT}, cat.get_category_types(0x4007))

        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x4E00..0x9FFF  KANJI\n")
            wf.write("0x4E8C KANJINUMERIC KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({CategoryType.KANJI}, cat.get_category_types(ord('男')))
        self.assertEqual({CategoryType.KANJI}, cat.get_category_types(0x4E8B))
        self.assertEqual({CategoryType.KANJI, CategoryType.KANJINUMERIC}, cat.get_category_types(0x4E8C))
        self.assertEqual({CategoryType.KANJI}, cat.get_category_types(0x4E8D))

    def test_read_character_definition_with_invalid_format(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0039\n")
        cat = charactercategory.CharacterCategory()
        with self.assertRaises(AttributeError) as cm:
            cat.read_character_definition(f)
        self.assertEqual('invalid format at line 0', cm.exception.args[0])

    def test_read_character_definition_with_invalid_range(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0029 NUMERIC\n")
        cat = charactercategory.CharacterCategory()
        with self.assertRaises(AttributeError) as cm:
            cat.read_character_definition(f)
        self.assertEqual('invalid range at line 0', cm.exception.args[0])

    def test_read_character_definition_with_invalid_type(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0039 FOO\n")
        cat = charactercategory.CharacterCategory()
        with self.assertRaises(AttributeError) as cm:
            cat.read_character_definition(f)
        self.assertEqual('FOO is invalid type at line 0', cm.exception.args[0])


if __name__ == '__main__':
    unittest.main()
