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

import mmap

from .dictionaryversion import has_grammar, has_synonym_group_ids, is_dictionary
from .dictionaryheader import DictionaryHeader
from .doublearraylexicon import DoubleArrayLexicon
from .grammar import Grammar


class BinaryDictionary(object):

    def __init__(self, bytes_: mmap.mmap, grammar: Grammar, header: DictionaryHeader, lexicon: DoubleArrayLexicon):
        self._bytes = bytes_
        self._grammar = grammar
        self._header = header
        self._lexicon = lexicon

    @staticmethod
    def _read_dictionary(filename, access=mmap.ACCESS_READ):
        with open(filename, 'rb') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=access)
        offset = 0
        header = DictionaryHeader.from_bytes(bytes_, offset)
        offset += header.storage_size()
        if not is_dictionary(header.version):
            raise Exception('invalid dictionary version')
        grammar = None
        if has_grammar(header.version):
            grammar = Grammar(bytes_, offset)
            offset += grammar.get_storage_size()

        lexicon = DoubleArrayLexicon(bytes_, offset, has_synonym_group_ids(header.version))
        return bytes_, grammar, header, lexicon

    @classmethod
    def from_system_dictionary(cls, filename):
        args = cls._read_dictionary(filename)
        if not args[2].is_system_dictionary():
            raise IOError('invalid system dictionary')
        return cls(*args)

    @classmethod
    def from_user_dictionary(cls, filename):
        args = cls._read_dictionary(filename, mmap.ACCESS_COPY)
        if not args[2].is_user_dictionary():
            raise IOError('invalid user dictionary')
        return cls(*args)

    def close(self):
        del self._grammar
        del self._lexicon
        self._bytes.close()

    @property
    def grammar(self) -> Grammar:
        return self._grammar

    @property
    def header(self) -> DictionaryHeader:
        return self._header

    @property
    def lexicon(self) -> DoubleArrayLexicon:
        return self._lexicon
