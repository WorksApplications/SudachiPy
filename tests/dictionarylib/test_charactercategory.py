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

from sudachipy.dictionarylib import categorytype, charactercategory


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
        self.assertEqual({categorytype.CategoryType.KANJI}, cat.get_category_types(ord('熙')))
        self.assertNotEqual({categorytype.CategoryType.DEFAULT}, cat.get_category_types(ord('熙')))

    def test_read_character_definition(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("#\n \n")
            wf.write("0x0030..0x0039 NUMERIC\n")
            wf.write("0x3007         KANJI\n")
            wf.write("0x0030         KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({categorytype.CategoryType.NUMERIC, categorytype.CategoryType.KANJI}, cat.get_category_types(0x0030))
        self.assertEqual({categorytype.CategoryType.NUMERIC}, cat.get_category_types(0x0039))
        self.assertEqual({categorytype.CategoryType.KANJI}, cat.get_category_types(0x3007))

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
