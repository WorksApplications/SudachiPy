import mmap
import unittest

from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib.dictionaryversion import DictionaryVersion
from sudachipy.dictionarylib.doublearraylexicon import DoubleArrayLexicon
from sudachipy.dictionarylib.grammar import Grammar


class TestDoubleArrayLexicon(unittest.TestCase):

    def setUp(self):
        # Copied from sudachipy.dictionay.Dictionary.read_system_dictionary
        filename = 'tests/resources/system.dic'
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        offset = 0
        self.header = DictionaryHeader(bytes_, offset)
        if self.header.version != DictionaryVersion.SYSTEM_DICT_VERSION:
            raise Exception("invalid system dictionary")
        offset += self.header.storage_size

        self.grammar = Grammar(bytes_, offset)
        offset += self.grammar.get_storage_size()
        self.lexicon = DoubleArrayLexicon(bytes_, offset)

    def test_lookup(self):
        res = self.lexicon.lookup('東京都'.encode('utf-8'), 0)
        self.assertEqual(3, len(res))
        self.assertEqual((4, 3), res[0])  # 東
        self.assertEqual((5, 6), res[1])  # 東京
        self.assertEqual((6, 9), res[2])  # 東京都

        res = self.lexicon.lookup('東京都に'.encode('utf-8'), 9)
        self.assertEqual(2, len(res))
        self.assertEqual((1, 12), res[0])  # に(接続助詞)
        self.assertEqual((2, 12), res[1])  # に(格助詞)

        res = self.lexicon.lookup('あれ'.encode('utf-8'), 0)
        self.assertEqual(0, len(res))

    def test_parameters(self):
        # た
        self.assertEqual(1, self.lexicon.get_left_id(0))
        self.assertEqual(1, self.lexicon.get_right_id(0))
        self.assertEqual(8729, self.lexicon.get_cost(0))

        # 東京都
        self.assertEqual(6, self.lexicon.get_left_id(6))
        self.assertEqual(8, self.lexicon.get_right_id(6))
        self.assertEqual(5320, self.lexicon.get_cost(6))

        # 都
        self.assertEqual(8, self.lexicon.get_left_id(9))
        self.assertEqual(8, self.lexicon.get_right_id(9))
        self.assertEqual(2914, self.lexicon.get_cost(9))

    def test_wordinfo(self):
        # た
        wi = self.lexicon.get_word_info(0)
        self.assertEqual('た', wi.surface)
        self.assertEqual(3, wi.head_word_length)
        self.assertEqual(0, wi.pos_id)
        self.assertEqual('た', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('た', wi.dictionary_form)
        self.assertEqual('タ', wi.reading_form)
        self.assertEqual([0], wi.a_unit_split)
        self.assertEqual([0], wi.b_unit_split)
        self.assertEqual([0], wi.word_structure)

        # 行っ
        wi = self.lexicon.get_word_info(8)
        self.assertEqual('行っ', wi.surface)
        self.assertEqual('行く', wi.normalized_form)
        self.assertEqual(7, wi.dictionary_form_word_id)
        self.assertEqual('行く', wi.dictionary_form)

        # 東京都
        wi = self.lexicon.get_word_info(6)
        self.assertEqual('東京都', wi.surface)
        self.assertEqual((5, 9), wi.a_unit_split)
        self.assertEqual([0], wi.b_unit_split)
        self.assertEqual((5, 9), wi.word_structure)

    def test_wordinfo_with_longword(self):
        # 0123456789 * 30
        wi = self.lexicon.get_word_info(36)
        self.assertEqual(300, len(wi.surface))
        self.assertEqual(300, wi.head_word_length)
        self.assertEqual(300, len(wi.normalized_form))
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual(300, len(wi.dictionary_form))
        self.assertEqual(570, len(wi.reading_form))

    def test_size(self):
        self.assertEqual(37, self.lexicon.size)


if __name__ == '__main__':
    unittest.main()
