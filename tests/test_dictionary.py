# This test file is ignored if it runs on .travis
# We probably need to parse user.dic to test this code.
import json
import os
import unittest

from sudachipy import tokenizer
from sudachipy.dictionary import Dictionary


class TestDictionary(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        with open(os.path.join(resource_dir, 'sudachi.json'), 'r') as rf:
            settings = json.load(rf)
        self.dict_ = Dictionary(settings, resource_dir)

    def tearDown(self) -> None:
        self.dict_.close()

    def test_create(self):
        self.assertEqual(tokenizer.Tokenizer, type(self.dict_.create()))

    def test_get_part_of_speech_size(self):
        self.assertEqual(9, self.dict_.grammar.get_part_of_speech_size())

    def test_get_part_of_speech_string(self):
        pos = self.dict_.grammar.get_part_of_speech_string(0)
        self.assertIsNotNone(pos)
        self.assertEqual('助動詞', pos[0])

    # def test_creat_with_merging_settings

    # def test_creat_with_merging_null_ settings


if __name__ == '__main__':
    unittest.main()
