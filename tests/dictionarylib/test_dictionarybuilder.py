import shutil
import tempfile
import unittest

from sudachipy.dictionarylib.dictionarybuilder import DictionaryBuilder


class TestDictionaryBuilder(unittest.TestCase):

    mocked_lexicon = None

    def mocked_size(self):
        return self.mocked_lexicon.size

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # self.mocked_lexicon = mock.Mock(spec=Lexicon)
        # self.mocked_lexicon.size.side_effect = self.mocked_size()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_decode(self):
        builder = DictionaryBuilder()
        org_text = '日本\\u1234東京'
        exp_text = '日本4660東京'
        self.assertEqual(exp_text, builder.decode(org_text))
        org_text = '日本\\u{1234}東京'
        exp_text = '日本4660東京'
        self.assertEqual(exp_text, builder.decode(org_text))

    def test_parseline(self):
        builder = DictionaryBuilder()
        entry = builder.parse_line(
            '京都,6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'.split(','))
        self.assertEqual('京都', entry.headword)
        self.assertEqual([6, 6, 5293], entry.parameters)
        self.assertEqual(0, entry.wordinfo.pos_id)
        self.assertEqual('*', entry.aunit_split_string)
        self.assertEqual('*', entry.bunit_split_string)

        entry = builder.parse_line(
            '京都,-1,-1,0,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'.split(','))
        self.assertIsNone(entry.headword)
        self.assertEqual(0, entry.wordinfo.pos_id)

    def test_parse_line_invalid_columns(self):
        builder = DictionaryBuilder()
        with self.assertRaises(ValueError) as cm:
            builder.parse_line('京都,6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*'.split(','))
        self.assertEqual('invalid format', cm.exception.args[0])

    def test_parse_line_empty_headword(self):
        builder = DictionaryBuilder()
        with self.assertRaises(ValueError) as cm:
            builder.parse_line(',6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'.split(','))
        self.assertEqual('headword is empty', cm.exception.args[0])

    def test_parse_line_toolong_headword(self):
        builder = DictionaryBuilder()
        x = 'a' * (32767 + 1) # max value of short in Java
        x = x + ',6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'
        with self.assertRaises(ValueError) as cm:
            builder.parse_line(x.split(','))
        self.assertEqual('string is too long', cm.exception.args[0])

    def test_parse_line_toomany_split(self):
        builder = DictionaryBuilder()
        with self.assertRaises(ValueError) as cm:
            builder.parse_line('京都,6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,B,0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0,*,*'.split(','))
        self.assertEqual('too many units', cm.exception.args[0])

    def test_parse_line_same_readingform(self):
        builder = DictionaryBuilder()
        entry = builder.parse_line('〒,6,6,5293,〒,名詞,普通名詞,一般,*,*,*,〒,〒,*,A,*,*,*'.split(','))
        self.assertEqual('〒', entry.wordinfo.reading_form)

    def test_add_to_trie(self):
        builder = DictionaryBuilder()
        builder.add_to_trie('abc', 0)
        builder.add_to_trie('abc', 1)
        builder.add_to_trie('abcd', 2)
        self.assertTrue(0 in builder.trie_keys['abc'.encode('utf-8')])
        self.assertTrue(1 in builder.trie_keys['abc'.encode('utf-8')])
