# Copyright (c) 2019 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import tempfile
import time
from io import StringIO
from logging import getLogger
from unittest import TestCase, mock

from sudachipy.dictionarylib import SYSTEM_DICT_VERSION
from sudachipy.dictionarylib.dictionarybuilder import DictionaryBuilder
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib.lexicon import Lexicon
from sudachipy.dictionarylib.userdictionarybuilder import UserDictionaryBuilder


class TestDictionaryBuilder(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.matrix_path = os.path.join(self.test_dir, 'matrix.txt')
        with open(self.matrix_path, 'w', encoding='utf-8') as wf:
            wf.write('1 1\n0 0 200\n')
        self.input_path = os.path.join(self.test_dir, 'input.txt')
        with open(self.input_path, 'w', encoding='utf-8') as wf:
            wf.write("東京都,0,0,0,東京都,名詞,固有名詞,地名,一般,*,*,ヒガシキョウト,東京都,*,B,\"東,名詞,普通名詞,一般,*,*,*,ヒガシ/2\",*,1/2\n")
            wf.write("東,-1,-1,0,東,名詞,普通名詞,一般,*,*,*,ヒガシ,ひがし,*,A,*,*,*\n")
            wf.write("京都,0,0,0,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*\n")
        self.logger = getLogger()
        self.logger.disabled = True

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parseline(self):
        builder = DictionaryBuilder(logger=self.logger)
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
        builder = DictionaryBuilder(logger=self.logger)
        with self.assertRaises(ValueError) as cm:
            builder.parse_line('京都,6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*'.split(','))
        self.assertEqual('invalid format', cm.exception.args[0])

    def test_parse_line_empty_headword(self):
        builder = DictionaryBuilder(logger=self.logger)
        with self.assertRaises(ValueError) as cm:
            builder.parse_line(',6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'.split(','))
        self.assertEqual('headword is empty', cm.exception.args[0])

    def test_parse_line_toolong_headword(self):
        builder = DictionaryBuilder(logger=self.logger)
        x = 'a' * (32767 + 1)  # max value of short in Java + 1
        x = x + ',6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,A,*,*,*'
        with self.assertRaises(ValueError) as cm:
            builder.parse_line(x.split(','))
        self.assertEqual('string is too long', cm.exception.args[0])

    def test_parse_line_toomany_split(self):
        builder = DictionaryBuilder(logger=self.logger)
        with self.assertRaises(ValueError) as cm:
            builder.parse_line('京都,6,6,5293,京都,名詞,固有名詞,地名,一般,*,*,キョウト,京都,*,B,0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0/0/1/2/3/4/5/6/7/8/9/0,*,*'.split(','))
        self.assertEqual('too many units', cm.exception.args[0])

    def test_parse_line_same_readingform(self):
        builder = DictionaryBuilder(logger=self.logger)
        entry = builder.parse_line('〒,6,6,5293,〒,名詞,普通名詞,一般,*,*,*,〒,〒,*,A,*,*,*'.split(','))
        self.assertEqual('〒', entry.wordinfo.reading_form)

    def test_add_to_trie(self):
        builder = DictionaryBuilder(logger=self.logger)
        builder.add_to_trie('abc', 0)
        builder.add_to_trie('abc', 1)
        builder.add_to_trie('abcd', 2)
        self.assertTrue(0 in builder.trie_keys['abc'.encode('utf-8')])
        self.assertTrue(1 in builder.trie_keys['abc'.encode('utf-8')])

    def test_convert_postable(self):
        builder = DictionaryBuilder(logger=self.logger)
        builder.convert_postable(['a,b,c,d,e,f', 'g,h,i,j,k,l'])
        self.assertEqual(2 + 3 * 12, builder.byte_buffer.tell())

    def test_convert_matrix(self):
        in_stream = StringIO('2 3\n0 0 0\n0 1 1\n0 2 2\n\n1 0 3\n1 1 4\n1 2 5\n')
        builder = DictionaryBuilder(logger=self.logger)
        matrix = builder.convert_matrix(in_stream)
        self.assertEqual(2, int.from_bytes(builder.byte_buffer.getvalue()[0:2], byteorder='little'))
        self.assertEqual(3, int.from_bytes(builder.byte_buffer.getvalue()[2:4], byteorder='little'))
        self.assertEqual(0, int.from_bytes(matrix.getvalue()[0:2], byteorder='little'))
        self.assertEqual(4, int.from_bytes(matrix.getvalue()[(2 + 1) * 2:(2 + 1) * 2 + 2], byteorder='little'))

    def test_decode(self):
        builder = DictionaryBuilder(logger=self.logger)
        self.assertEqual('a,c', builder.decode('a\\u002cc'))
        self.assertEqual('a,c', builder.decode('a\\u{002c}c'))
        self.assertEqual('a𠮟c', builder.decode('a\\u{20b9f}c'))

    def test_parse_splitinfo(self):
        builder = DictionaryBuilder(logger=self.logger)
        builder.entries.extend([None] * 4)
        self.assertEqual([], builder.parse_splitinfo('*'))
        self.assertEqual([1, 2, 3], builder.parse_splitinfo('1/2/3'))
        self.assertEqual(2, builder.parse_splitinfo('1/U2/3')[1])

        mocked_lexicon = mock.Mock(spec=Lexicon)
        mocked_lexicon.size.return_value = 4
        builder = UserDictionaryBuilder(None, mocked_lexicon)
        builder.entries += [None, None, None]
        self.assertEqual([1, 2 | 1 << 28, 3], builder.parse_splitinfo("1/U2/3"))

    def test_parse_splitinfo_invalid_wordid(self):
        builder = DictionaryBuilder(logger=self.logger)
        with self.assertRaises(ValueError) as cm:
            builder.parse_splitinfo('1/2/3')
        self.assertEqual('invalid word ID', cm.exception.args[0])

    def test_parse_splitinfo_invalid_wordid_userdict(self):
        mocked_lexicon = mock.Mock(spec=Lexicon)
        mocked_lexicon.size.return_value = 1
        builder = UserDictionaryBuilder(None, mocked_lexicon)
        with self.assertRaises(ValueError) as cm:
            builder.parse_splitinfo('0/U1')
        self.assertEqual('invalid word ID', cm.exception.args[0])

    def test_parse_splitinfo_invalid_system_wordid_in_userdict(self):
        mocked_lexicon = mock.Mock(spec=Lexicon)
        mocked_lexicon.size.return_value = 1
        builder = UserDictionaryBuilder(None, mocked_lexicon)
        builder.entries.append(None)
        with self.assertRaises(ValueError) as cm:
            builder.parse_splitinfo('1/U0')
        self.assertEqual('invalid word id', cm.exception.args[0])
        pass

    def test_write_string(self):
        builder = DictionaryBuilder(logger=self.logger)
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
        builder = DictionaryBuilder(logger=self.logger)
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
        matrix_input_stream = open(self.matrix_path, 'r', encoding='utf-8')

        header = DictionaryHeader(SYSTEM_DICT_VERSION, int(time.time()), 'test')
        out_stream.write(header.to_bytes())
        builder = DictionaryBuilder(logger=self.logger)
        builder.build(lexicon_paths, matrix_input_stream, out_stream)
        out_stream.close()
        matrix_input_stream.close()

        buffers, header, grammar, lexicon_set = self.read_system_dictionary(out_path)
        lexicon = lexicon_set.lexicons[0]

        # header
        self.assertEqual(SYSTEM_DICT_VERSION, header.version)
        self.assertEqual('test', header.description)

        # grammar
        self.assertEqual(2, grammar.get_part_of_speech_size())
        self.assertEqual(["名詞", "固有名詞", "地名", "一般", "*", "*"], grammar.get_part_of_speech_string(0))
        self.assertEqual(["名詞", "普通名詞", "一般", "*", "*", "*"], grammar.get_part_of_speech_string(1))
        self.assertEqual(200, grammar.get_connect_cost(0, 0))

        # lexicon
        self.assertEqual(3, lexicon.size())
        self.assertEqual(0, lexicon.get_cost(0))
        wi = lexicon.get_word_info(0)
        self.assertEqual('東京都', wi.surface)
        self.assertEqual('東京都', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('ヒガシキョウト', wi.reading_form)
        self.assertEqual(0, wi.pos_id)
        self.assertEqual([1, 2], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        lst = lexicon.lookup('東京都'.encode('utf-8'), 0)
        self.assertEqual((0, len('東京都'.encode('utf-8'))), lst.__next__())
        with self.assertRaises(StopIteration):
            lst.__next__()

        self.assertEqual(-1, lexicon.get_left_id(1))
        self.assertEqual(0, lexicon.get_cost(1))
        wi = lexicon.get_word_info(1)
        self.assertEqual('東', wi.surface)
        self.assertEqual('ひがし', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('ヒガシ', wi.reading_form)
        self.assertEqual(1, wi.pos_id)
        self.assertEqual([], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        lst = lexicon.lookup('東'.encode('utf-8'), 0)
        with self.assertRaises(StopIteration):
            lst.__next__()

    @staticmethod
    def read_system_dictionary(filename):
        """
        Copy of sudachipy.dictionary.Dictionary.read_system_dictionary
        :param filename:
        :return:
        """
        import mmap
        from sudachipy import dictionarylib
        buffers = []
        if filename is None:
            raise AttributeError("system dictionary is not specified")
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        buffers.append(bytes_)

        offset = 0
        header = dictionarylib.dictionaryheader.DictionaryHeader.from_bytes(bytes_, offset)
        if header.version != SYSTEM_DICT_VERSION:
            raise Exception("invalid system dictionary")
        offset += header.storage_size()

        grammar = dictionarylib.grammar.Grammar(bytes_, offset)
        offset += grammar.get_storage_size()

        lexicon = dictionarylib.lexiconset.LexiconSet(dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, offset))
        return buffers, header, grammar, lexicon
