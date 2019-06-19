import os
import shutil
import tempfile
import time
import unittest


from sudachipy.dictionarylib.dictionarybuilder import DictionaryBuilder
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib.dictionaryversion import DictionaryVersion


class TestDictionaryBuilder(unittest.TestCase):

    mocked_lexicon = None

    def mocked_size(self):
        return self.mocked_lexicon.size

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.matrix_path = os.path.join(self.test_dir, 'matrix.txt')
        with open(self.matrix_path, 'w') as wf:
            wf.write('1 1\n0 0 200\n')
        self.input_path = os.path.join(self.test_dir, 'input.txt')
        with open(self.input_path, 'w') as wf:
            wf.write("東京都,0,0,0,東京都,名詞,固有名詞,地名,一般,*,*,ヒガシキョウト,東京都,*,B,\"東,名詞,普通名詞,一般,*,*,*,ヒガシ/2\",*,1/2\n")
            wf.write("東,-1,-1,0,東,名詞,普通名詞,一般,*,*,*,ヒガシ,ひがし,*,A,*,*,*\n")
            wf.write("京都,0,0,0,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*\n")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

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
        x = 'a' * (32767 + 1)  # max value of short in Java + 1
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

    def test_convert_postable(self):
        builder = DictionaryBuilder()
        builder.convert_postable(['a,b,c,d,e,f', 'g,h,i,j,k,l'])
        self.assertEqual(2 + 3 * 12, builder.byte_buffer.tell())

    def test_convert_matrix(self):
        from io import StringIO
        in_stream = StringIO('2 3\n0 0 0\n0 1 1\n0 2 2\n\n1 0 3\n1 1 4\n1 2 5\n')
        builder = DictionaryBuilder()
        matrix = builder.convert_matrix(in_stream)
        self.assertEqual(2, int.from_bytes(builder.byte_buffer.getvalue()[0:2], byteorder='little'))
        self.assertEqual(3, int.from_bytes(builder.byte_buffer.getvalue()[2:4], byteorder='little'))
        self.assertEqual(0, int.from_bytes(matrix.getvalue()[0:2], byteorder='little'))
        self.assertEqual(4, int.from_bytes(matrix.getvalue()[(2 + 1) * 2:(2 + 1) * 2 + 2], byteorder='little'))

    def test_decode(self):
        builder = DictionaryBuilder()
        self.assertEqual('a,c', builder.decode('a\\u002cc'))
        self.assertEqual('a,c', builder.decode('a\\u{002c}c'))
        self.assertEqual('a𠮟c', builder.decode('a\\u{20b9f}c'))

    def test_parse_splitinfo(self):
        builder = DictionaryBuilder()
        builder.entries.extend([None] * 4)
        self.assertEqual([], builder.parse_splitinfo('*'))
        self.assertEqual([1, 2, 3], builder.parse_splitinfo('1/2/3'))
        self.assertEqual(2, builder.parse_splitinfo('1/U2/3')[1])
        # Todo: add test for UserDictionaryBuilder

    def test_parse_splitinfo_invalid_wordid(self):
        builder = DictionaryBuilder()
        with self.assertRaises(ValueError) as cm:
            builder.parse_splitinfo('1/2/3')
        self.assertEqual('invalid word ID', cm.exception.args[0])

    def test_parse_splitinfo_invalid_system_wordid_in_userdict(self):
        # Todo: add test for UserDictionaryBuilder
        pass

    def test_write_string(self):
        builder = DictionaryBuilder()
        position = builder.byte_buffer.tell()
        builder.write_string('')
        self.assertEqual(0, builder.byte_buffer.getvalue()[position])
        self.assertEqual(position + 1, builder.byte_buffer.tell())

        position = builder.byte_buffer.tell()
        builder.write_string('あ𠮟')
        self.assertEqual(3, builder.byte_buffer.getvalue()[position])
        self.assertEqual('あ', builder.byte_buffer.getvalue()[position + 1: position + 3].decode('utf-16-le'))
        a = int.from_bytes(builder.byte_buffer.getvalue()[position + 3: position + 5], byteorder='little')
        b = int.from_bytes(builder.byte_buffer.getvalue()[position + 5: position + 7], byteorder='little')
        self.assertEqual(55362, a)  # \ud842
        self.assertEqual(57247, b)  # \udf94

        position = builder.byte_buffer.tell()
        long_str = '0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
        len_ = len(long_str)
        builder.write_string(long_str)
        self.assertEqual((len_ >> 8) | 0x80, builder.byte_buffer.getvalue()[position])
        self.assertEqual(len_ & 0xff, builder.byte_buffer.getvalue()[position + 1])
        self.assertEqual(position + 2 + 2 * len_, builder.byte_buffer.tell())

    def test_write_intarray(self):
        builder = DictionaryBuilder()
        position = builder.byte_buffer.tell()
        builder.write_intarray([])
        self.assertEqual(0, builder.byte_buffer.getvalue()[position])
        builder.write_intarray([1, 2, 3])
        self.assertEqual(3, builder.byte_buffer.getvalue()[position + 1])
        self.assertEqual(1, int.from_bytes(builder.byte_buffer.getvalue()[position + 2:position + 6], byteorder='little', signed=True))
        self.assertEqual(2, int.from_bytes(builder.byte_buffer.getvalue()[position + 6:position + 10], byteorder='little', signed=True))
        self.assertEqual(3, int.from_bytes(builder.byte_buffer.getvalue()[position + 10:position + 14], byteorder='little', signed=True))

    def test_build(self):
        out_path = os.path.join(self.test_dir, 'output.txt')

        out_stream = open(out_path, 'wb')
        lexicon_paths = [self.input_path]
        matrix_input_stream = open(self.matrix_path)

        header = DictionaryHeader.from_items(DictionaryVersion.SYSTEM_DICT_VERSION, int(time.time()), 'test')
        out_stream.write(header.bytes_)
        builder = DictionaryBuilder()
        builder.build(lexicon_paths, matrix_input_stream, out_stream)
        out_stream.close()
        matrix_input_stream.close()
