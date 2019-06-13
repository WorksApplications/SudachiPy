import json
import unittest

from sudachipy import config, dictionary


class TestDoubleArrayLexicon(unittest.TestCase):

    def setUp(self):
        with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.dict_ = None
        try:
            self.dict_ = dictionary.Dictionary(settings)
        except FileNotFoundError:
            self.fail('dictionary isn\'t prepared properly')

    def test_lookup(self):
        res = self.dict_.lexicon.lookup('東京都'.encode('utf-8'), 0)
        self.assertEqual(14, len(res))
        self.assertEqual([(513765, 3),
                          (513766, 3),
                          (513767, 3),
                          (513768, 3),
                          (513769, 3),
                          (513770, 3),
                          (513771, 3),
                          (513772, 3),
                          (513773, 3),
                          (513774, 3),
                          (513775, 3),
                          (513776, 3),
                          (513823, 6),
                          (1286193, 9)], res)
        res = self.dict_.lexicon.lookup('東京都に'.encode('utf-8'), 9)
        self.assertEqual(11, len(res))
        self.assertEqual([(114117, 12),
                          (114118, 12),
                          (114119, 12),
                          (114120, 12),
                          (114121, 12),
                          (114122, 12),
                          (114123, 12),
                          (114124, 12),
                          (114125, 12),
                          (114126, 12),
                          (114127, 12)], res)
        res = self.dict_.lexicon.lookup('あれ'.encode('utf-8'), 0)
        self.assertEqual(13, len(res))


if __name__ == '__main__':
    unittest.main()
