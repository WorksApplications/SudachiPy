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

import json
import os
import shutil
import tempfile
import time
from logging import getLogger
from unittest import TestCase

from sudachipy.dictionary import Dictionary
from sudachipy.dictionarylib import SYSTEM_DICT_VERSION_2
from sudachipy.dictionarylib.dictionarybuilder import DictionaryBuilder
from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader


class TestSwitchDictionary(TestCase):

    def setUp(self):
        self.logger = getLogger()
        self.logger.disabled = True

        self.temp_dir = tempfile.mkdtemp()
        self.resource_dir = os.path.join(self.temp_dir, 'resources')
        os.makedirs(self.resource_dir)

        test_resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.char_def_path = os.path.join(self.resource_dir, 'char.def')
        shutil.copy(os.path.join(test_resource_dir, 'char.def'), self.char_def_path)

        self.sudachi_json_path = os.path.join(self.resource_dir, 'sudachi.json')
        shutil.copy(os.path.join(test_resource_dir, 'sudachi.json'), self.sudachi_json_path)
        self._rewrite_json(self.sudachi_json_path, 'userDict', [])

        self.matrix_path = os.path.join(self.resource_dir, 'matrix.txt')
        with open(self.matrix_path, 'w', encoding='utf-8') as wf:
            wf.write('1 1\n0 0 200\n')

        small_lexs = ["島,0,0,0,島,名詞,普通名詞,一般,*,*,*,シマ,島,*,A,*,*,*"]
        core_lexs = ["徳島本町,0,0,0,徳島本町,名詞,固有名詞,地名,一般,*,*,トクシマホンチョウ,徳島本町,*,A,*,*,*,*"]
        notcore_lexs = ["徳島堰,0,0,0,徳島堰,名詞,固有名詞,一般,*,*,*,トクシマセギ,徳島堰,*,A,*,*,*"]

        small_lines = small_lexs
        core_lines = small_lexs + core_lexs
        full_lines = small_lexs + core_lexs + notcore_lexs

        self.small_txt_path = os.path.join(self.resource_dir, 'small.csv')
        self.core_txt_path = os.path.join(self.resource_dir, 'core.csv')
        self.full_txt_path = os.path.join(self.resource_dir, 'full.csv')

        self.small_dic_path = self._build_dictionary(self.small_txt_path, small_lines, 'small.dic')
        self.core_dic_path = self._build_dictionary(self.core_txt_path, core_lines, 'core.dic')
        self.full_dic_path = self._build_dictionary(self.full_txt_path, full_lines, 'full.dic')

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @staticmethod
    def _rewrite_json(json_file_path, k, v):
        with open(json_file_path, 'r') as f:
            obj = json.load(f)
        obj[k] = v
        with open(json_file_path, 'w') as f:
            json.dump(obj, f, ensure_ascii=False, indent=4)

    def _build_dictionary(self, input_txt_path, lex_lines, dictionary_name):
        with open(input_txt_path, 'w', encoding='utf-8') as wf:
            wf.write("\n".join(lex_lines))

        out_path = os.path.join(self.resource_dir, dictionary_name)
        out_stream = open(out_path, 'wb')
        lexicon_paths = [input_txt_path]
        matrix_input_stream = open(self.matrix_path, 'r', encoding='utf-8')

        header = DictionaryHeader(SYSTEM_DICT_VERSION_2, int(time.time()), 'test')
        out_stream.write(header.to_bytes())
        builder = DictionaryBuilder(logger=self.logger)
        builder.build(lexicon_paths, matrix_input_stream, out_stream)
        out_stream.close()
        matrix_input_stream.close()

        return out_path

    def test_switch_dictionary(self):
        self._rewrite_json(self.sudachi_json_path, 'systemDict', 'small.dic')  # relative path
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(1, self.dict.lexicon.size())
        self._rewrite_json(self.sudachi_json_path, 'systemDict', self.small_dic_path)  # abstract path
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(1, self.dict.lexicon.size())

        self._rewrite_json(self.sudachi_json_path, 'systemDict', 'core.dic')
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(2, self.dict.lexicon.size())
        self._rewrite_json(self.sudachi_json_path, 'systemDict', self.core_dic_path)
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(2, self.dict.lexicon.size())

        self._rewrite_json(self.sudachi_json_path, 'systemDict', 'full.dic')
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(3, self.dict.lexicon.size())
        self._rewrite_json(self.sudachi_json_path, 'systemDict', self.full_dic_path)
        self.dict = Dictionary(config_path=self.sudachi_json_path, resource_dir=self.resource_dir)
        self.assertEqual(3, self.dict.lexicon.size())
