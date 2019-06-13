import os
import shutil
import tempfile
import unittest

from sudachipy.dictionarylib import charactercategory, categorytype


class TestCharacterCategory(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
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
        cat.read_character_definition('tests/resources/char.def')
        self.assertEqual({categorytype.CategoryType.KANJI}, cat.get_category_types(ord('熙')))
        self.assertNotEqual({categorytype.CategoryType.DEFAULT}, cat.get_category_types(ord('熙')))

    def test_read_character_definition(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("#\n \n")
            wf.write("0x0030..0x0039 NUMERIC\n")
            wf.write("0x3007         KANJI\n")
        cat = charactercategory.CharacterCategory()
        cat.read_character_definition(f)
        self.assertEqual({categorytype.CategoryType.NUMERIC}, cat.get_category_types(0x0030))
        self.assertEqual({categorytype.CategoryType.NUMERIC}, cat.get_category_types(0x0039))
        self.assertEqual({categorytype.CategoryType.KANJI}, cat.get_category_types(0x3007))

    def test_read_character_definition_with_invalid_format(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0039\n")
        cat = charactercategory.CharacterCategory()
        try:
            cat.read_character_definition(f)
            self.fail('no exception detected')
        except AttributeError:
            pass

    def test_read_character_definition_with_invalid_range(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0029 NUMERIC\n")
        cat = charactercategory.CharacterCategory()
        try:
            cat.read_character_definition(f)
            self.fail('no exception detected')
        except AttributeError:
            pass

    def test_read_character_definition_with_invalid_type(self):
        f = os.path.join(self.test_dir, 'test_file.txt')
        with open(f, 'w') as wf:
            wf.write("0x0030..0x0039 FOO\n")
        cat = charactercategory.CharacterCategory()
        try:
            cat.read_character_definition(f)
            self.fail('no exception detected')
        except AttributeError:
            pass


if __name__ == '__main__':
    unittest.main()
