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
