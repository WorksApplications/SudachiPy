import os
import unittest

from sudachipy import dictionary


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.dict_ = dictionary.Dictionary(os.path.join(resource_dir, 'sudachi.json'), resource_dir)
        self.tokenizer_obj = self.dict_.create()

    def test_tokenize_small_katanana_only(self):
        ms = self.tokenizer_obj.tokenize('ァ')
        self.assertEqual(1, len(ms))

    def test_part_of_speech(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, len(ms))
        m = ms[0]
        pid = m.part_of_speech_id()
        self.assertTrue(self.dict_.grammar.get_part_of_speech_size() > pid)
        pos = m.part_of_speech()
        self.assertEqual(pos, self.dict_.grammar.get_part_of_speech_string(pid))

    def test_get_word_id(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, len(ms))

        wid = ms[0].word_id()
        ms = self.tokenizer_obj.tokenize('ぴらる')
        self.assertEqual(1, len(ms))
        self.assertNotEqual(wid, ms[0].word_id())

        ms = self.tokenizer_obj.tokenize('京')
        self.assertEqual(1, len(ms))

    def test_get_dictionary_id(self):
        ms = self.tokenizer_obj.tokenize('京都')
        self.assertEqual(1, ms.size())
        self.assertEqual(0, ms[0].dictionary_id())

        ms = self.tokenizer_obj.tokenize('ぴらる')
        self.assertEqual(1, ms.size())
        self.assertEqual(1, ms[0].dictionary_id())

        ms = self.tokenizer_obj.tokenize('京')
        self.assertEqual(1, ms.size())
        self.assertTrue(ms[0].dictionary_id() < 0)


if __name__ == '__main__':
    unittest.main()
