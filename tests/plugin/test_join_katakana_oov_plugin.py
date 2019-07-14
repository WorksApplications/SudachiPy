import os
import unittest

from sudachipy.config import settings
from sudachipy.dictionary import Dictionary
from sudachipy.plugin.path_rewrite import JoinKatakanaOovPlugin
from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder


class TestJoinKatakanaOOVPlugin(unittest.TestCase):

    def setUp(self):
        resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'resources')
        self.dict_ = Dictionary(os.path.join(resource_dir, 'sudachi.json'), resource_dir)
        self.tokenizer = self.dict_.create()
        self.plugin = JoinKatakanaOovPlugin(settings['pathRewritePlugin'][1])

    def test_katakana_length(self):
        # アイ, アイウ in the dictionary
        self.plugin._min_length = 0
        path = self.get_path('アイアイウ')
        self.assertEqual(2, len(path))

        self.plugin._min_length = 1
        path = self.get_path('アイアイウ')
        self.assertEqual(2, len(path))

        self.plugin._min_length = 2
        path = self.get_path('アイアイウ')
        self.assertEqual(2, len(path))

        self.plugin._min_length = 3
        path = self.get_path('アイアイウ')
        self.assertEqual(1, len(path))

    def test_pos(self):
        # アイアイウ is 名詞-固有名詞-地名-一般 in the dictionary
        self.plugin._min_length = 3
        path = self.get_path('アイアイウ')
        self.assertEqual(1, len(path))
        self.assertFalse(path[0].is_oov())

    def test_starts_with_middle(self):
        self.plugin._min_length = 3
        path = self.get_path('アイウアイアイウ')
        self.assertEqual(1, len(path))

    def test_starts_with_tail(self):
        self.plugin._min_length = 3
        path = self.get_path('アイウアイウアイ')
        self.assertEqual(1, len(path))

    def test_with_nooovbow(self):
        self.plugin._min_length = 3
        path = self.get_path('ァアイアイウ')
        self.assertEqual(2, len(path))
        self.assertEqual('ァ', path[0].get_word_info().surface)

        path = self.get_path('アイウァアイウ')
        self.assertEqual(1, len(path))

    def get_path(self, text: str):
        input_ = UTF8InputTextBuilder(text, self.tokenizer.grammar).build()
        self.tokenizer.build_lattice(input_)
        path = self.tokenizer.lattice.get_best_path()
        self.plugin.rewrite(input_, path, self.tokenizer.lattice)
        self.tokenizer.lattice.clear()
        return path


if __name__ == '__main__':
    unittest.main()
