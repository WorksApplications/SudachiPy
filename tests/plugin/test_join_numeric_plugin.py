import unittest
# import os
# from sudachipy.dictionary import Dictionary
# from sudachipy.plugin.path_rewrite import JoinNumericPlugin
# from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder


class TestJoinNumericOOVPlugin(unittest.TestCase):
    """
    Implementation of JoinNumericOOVPlugin is out of date,
    NumericParser required beforehand
    """

    def setUp(self):
        pass
    #     resource_dir = os.path.join(os.pardir, 'resources')
    #     self.dict_ = Dictionary(os.path.join(resource_dir, 'sudachi.json'), resource_dir)
    #     self.tokenizer = self.dict_.create()
    #     self.plugin = JoinNumericPlugin(None)
    #     self.plugin.set_up(self.dict_.grammar)
    #
    # def test_digit(self):
    #     path = self.get_path('123円20銭')
    #     self.assertEqual(4, len(path))
    #     self.assertEqual('123', path[0].get_word_info().surface)
    #     self.assertEqual('20', path[2].get_word_info().surface)
    #
    #     path = self.get_path('080-121')
    #     self.assertEqual(3, len(path))
    #     self.assertEqual('080', path[0].get_word_info().surface)
    #     self.assertEqual('121', path[1].get_word_info().surface)
    #
    # def get_path(self, text: str):
    #     input_ = UTF8InputTextBuilder(text, self.tokenizer.grammar).build()
    #     self.tokenizer.build_lattice(input_)
    #     path = self.tokenizer.lattice.get_best_path()
    #     self.plugin.rewrite(input_, path, self.tokenizer.lattice)
    #     self.tokenizer.lattice.clear()
    #     return path


if __name__ == '__main__':
    unittest.main()
