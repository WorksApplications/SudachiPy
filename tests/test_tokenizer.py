import json
import unittest

from sudachipy import config, dictionary, tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        # It's impossible to avoid to use test dictionary
        # See implementation of dictionary.Dictionary
        with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.dict_ = None
        self.tokenizer_obj = None
        try:
            self.dict_ = dictionary.Dictionary(settings)
            self.tokenizer_obj = self.dict_.create()
        except FileNotFoundError:
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

    def test_multi_granular(self):
        text = '医薬品安全管理責任者'
        mode = tokenizer.Tokenizer.SplitMode.C
        tokenized = [m.surface() for m in self.tokenizer_obj.tokenize(mode, text)]
        self.assertEqual(['医薬品', '安全', '管理責任者'], tokenized)
        mode = tokenizer.Tokenizer.SplitMode.B
        tokenized = [m.surface() for m in self.tokenizer_obj.tokenize(mode, text)]
        self.assertEqual(['医薬品', '安全', '管理', '責任者'], tokenized)
        mode = tokenizer.Tokenizer.SplitMode.A
        tokenized = [m.surface() for m in self.tokenizer_obj.tokenize(mode, text)]
        self.assertEqual(['医薬', '品', '安全', '管理', '責任', '者'], tokenized)

    def test_morpheme(self):
        mode = tokenizer.Tokenizer.SplitMode.A
        m = self.tokenizer_obj.tokenize(mode, '食べ')[0]
        self.assertEqual('食べ', m.surface())
        self.assertEqual('食べる', m.dictionary_form())
        self.assertEqual('タベ', m.reading_form())
        self.assertEqual(['動詞', '一般', '*', '*', '下一段-バ行', '連用形-一般'], m.part_of_speech())

    def test_normalize(self):
        mode = tokenizer.Tokenizer.SplitMode.A
        self.assertEqual('付属', self.tokenizer_obj.tokenize(mode, '附属')[0].normalized_form())
        self.assertEqual('サマー', self.tokenizer_obj.tokenize(mode, "SUMMER")[0].normalized_form())
        self.assertEqual('シミュレーション', self.tokenizer_obj.tokenize(mode, "シュミレーション")[0].normalized_form())


if __name__ == '__main__':
    unittest.main()
