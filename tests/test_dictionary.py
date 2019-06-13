import json
import unittest
import os
from sudachipy import config, dictionary, tokenizer


class TestDictionary(unittest.TestCase):

    def setUp(self):
        with open('tests/resources/sudachi.json', "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.dict_ = None
        try:
            self.dict_ = dictionary.Dictionary(settings)
        except FileNotFoundError:
            self.fail('dictionary isn\'t prepared properly')

    def test_create(self):
        self.assertEqual(tokenizer.Tokenizer, type(self.dict_.create()))

    # def test_close(self):
    #     self.dict_.close()

    # def test_get_part_of_speech_size(self):
    #     self.assertEqual(8, self.dict_.grammar.get_part_of_speech_size())

    # def test_get_part_of_speech_string(self):
    #     pos = self.dict_.grammar.get_part_of_speech_string(0)
    #     self.assertIsNotNone(pos)
    #     self.assertEqual('助動詞', pos[0])


if __name__ == '__main__':
    unittest.main()
