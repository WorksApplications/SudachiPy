import json
import unittest

from sudachipy import config, dictionary


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.dict_ = None
        self.tokenizer_obj = None
        try:
            self.dict_ = dictionary.Dictionary(settings)
            self.tokenizer_obj = self.dict_.create()
        except FileNotFoundError as e:
            self.fail('dictionary isn\'t prepared properly')

    def test_tokenize_small_katanana_only(self):
        ms = self.tokenizer_obj.tokenize(None, 'ァ')
        self.assertEqual(1, len(ms))

    def test_part_of_speech(self):
        ms = self.tokenizer_obj.tokenize(None, '京都')
        self.assertEqual(1, len(ms))
        m = ms[0]
        pid = m.part_of_speech_id()
        self.assertTrue(self.dict_.grammar.get_part_of_speech_size() > pid)
        pos = m.part_of_speech()
        self.assertEqual(pos, self.dict_.grammar.get_part_of_speech_string(pid))

    def test_get_word_id(self):
        ms = self.tokenizer_obj.tokenize(None, '京都')
        self.assertEqual(1, len(ms))
        # wid = ms[0].word_id()

        # test for user dictionary
        # ms = self.tokenizer_obj.tokenize(None, 'ぴらる')
        # self.assertEqual(1, len(ms))
        # self.assertNotEqual(wid, ms[0].word_id())

        ms = self.tokenizer_obj.tokenize(None, '京')
        self.assertEqual(1, len(ms))


if __name__ == '__main__':
    unittest.main()
