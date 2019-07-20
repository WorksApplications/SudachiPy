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
from logging import getLogger
from unittest import TestCase

from sudachipy.dictionarylib import SYSTEM_DICT_VERSION
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib.userdictionarybuilder import UserDictionaryBuilder

from .test_dictionarybuilder import TestDictionaryBuilder


class TestUserDictionaryBuilder(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')
        self.dict_filename = os.path.join(test_resources_dir, 'system.dic')
        _, _, self.grammar, self.lexicon_set = \
            TestDictionaryBuilder.read_system_dictionary(self.dict_filename)
        self.logger = getLogger()
        self.logger.disabled = True

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parseline_with_userdefined_POS(self):
        builder = UserDictionaryBuilder(self.grammar, self.lexicon_set, logger=self.logger)
        builder.parse_line('田中,0,0,0,田中,存在,しない,品詞,*,*,*,タナカ,田中,*,A,*,*,*\n'.split(','))
        self.assertEqual(1, len(builder.pos_table.get_list()))

    def test_build(self):
        out_path = os.path.join(self.test_dir, 'output.txt')
        in_path = os.path.join(self.test_dir, 'input.txt')

        out_stream = open(out_path, 'wb')
        # lexicon_paths = [self.input_path]
        # matrix_input_stream = open(self.matrix_path, 'r')
        with open(in_path, 'w', encoding='utf-8') as wf:
            wf.write("東京都市,0,0,0,東京都市,名詞,固有名詞,地名,一般,*,*,ヒガシキョウトシ,東京都市,*,B,\"東,名詞,普通名詞,一般,*,*,*,ヒガシ/3/U1\",*,\"4/3/市,名詞,普通名詞,一般,*,*,*,シ\"\n")
            wf.write('市,-1,-1,0,市,名詞,普通名詞,一般,*,*,*,シ,市,*,A,*,*,*\n')

        _, _, grammar, lexicon_set = TestDictionaryBuilder.read_system_dictionary(self.dict_filename)
        header = DictionaryHeader(SYSTEM_DICT_VERSION, int(time.time()), 'test')
        out_stream.write(header.to_bytes())
        builder = UserDictionaryBuilder(grammar, lexicon_set, logger=self.logger)
        lexicon_paths = [in_path]
        builder.build(lexicon_paths, None, out_stream)
        out_stream.close()

        buffers, header, grammar, lexicon_set = TestDictionaryBuilder.read_system_dictionary(out_path)
        lexicon = lexicon_set.lexicons[0]

        # header
        self.assertEqual(SYSTEM_DICT_VERSION, header.version)
        self.assertEqual('test', header.description)

        # lexicon
        self.assertEqual(0, lexicon.get_left_id(0))
        self.assertEqual(0, lexicon.get_cost(0))
        wi = lexicon.get_word_info(0)
        self.assertEqual('東京都市', wi.surface)
        self.assertEqual('東京都市', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('ヒガシキョウトシ', wi.reading_form)
        self.assertEqual(3, wi.pos_id)
        self.assertEqual([4, 3, 1 | (1 << 28)], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        self.assertEqual([4, 3, 1 | (1 << 28)], wi.word_structure)
        lst = lexicon.lookup('東京都市'.encode('utf-8'), 0)
        self.assertEqual((0, len('東京都市'.encode('utf-8'))), lst.__next__())
        with self.assertRaises(StopIteration):
            lst.__next__()

        self.assertEqual(-1, lexicon.get_left_id(1))
        self.assertEqual(0, lexicon.get_cost(1))
        wi = lexicon.get_word_info(1)
        self.assertEqual('市', wi.surface)
        self.assertEqual('市', wi.normalized_form)
        self.assertEqual(-1, wi.dictionary_form_word_id)
        self.assertEqual('シ', wi.reading_form)
        self.assertEqual(4, wi.pos_id)
        self.assertEqual([], wi.a_unit_split)
        self.assertEqual([], wi.b_unit_split)
        lst = lexicon.lookup('東'.encode('utf-8'), 0)
        with self.assertRaises(StopIteration):
            lst.__next__()
