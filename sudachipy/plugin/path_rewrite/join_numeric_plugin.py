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

import warnings

from sudachipy.dictionarylib.categorytype import CategoryType

from .numericparser import NumericParser
from .path_rewrite_plugin import PathRewritePlugin


class JoinNumericPlugin(PathRewritePlugin):

    _numeric_pos_id = None
    _enable_normalize = True

    def __init__(self, json_obj):
        self._NUMERIC_POS = ['名詞', '数詞', '*', '*', '*', '*']
        if not json_obj:
            return
        if 'joinKanjiNumeric' in json_obj:
            warnings.warn('joinKanjiNumeric is already nonsense key', SyntaxWarning)
        if 'enableNormalize' in json_obj:
            self._enable_normalize = json_obj['enableNormalize']

    def set_up(self, grammar):
        self._numeric_pos_id = grammar.get_part_of_speech_id(self._NUMERIC_POS)

    def rewrite(self, text, path, lattice):
        begin_index = -1
        comma_as_digit = True
        period_as_digit = True
        parser = NumericParser()
        i = -1

        while i < len(path) - 1:
            i += 1
            node = path[i]
            types = self.get_char_category_types(text, node)
            s = node.get_word_info().normalized_form
            if CategoryType.NUMERIC in types or CategoryType.KANJINUMERIC in types or \
               (period_as_digit and s == '.') or (comma_as_digit and s == ','):

                if begin_index < 0:
                    parser.clear()
                    begin_index = i

                for c in s:
                    if not parser.append(c):
                        if begin_index >= 0:
                            if parser.error_state == NumericParser.Error.COMMA:
                                comma_as_digit = False
                                i = begin_index - 1
                            elif parser.error_state == NumericParser.Error.POINT:
                                period_as_digit = False
                                i = begin_index - 1
                            begin_index = -1
                        break
                continue

            if begin_index >= 0:
                if parser.done():
                    self._concat(path, begin_index, i, lattice, parser)
                    i = begin_index + 1
                else:
                    ss = path[i - 1].get_word_info().normalized_form
                    if (parser.error_state == NumericParser.Error.COMMA and ss == ',') or \
                       (parser.error_state == NumericParser.Error.POINT and ss == '.'):
                        self._concat(path, begin_index, i - 1, lattice, parser)
                        i = begin_index + 2
            begin_index = -1
            if not comma_as_digit and s != ',':
                comma_as_digit = True
            if not period_as_digit and s != '.':
                period_as_digit = True

        if begin_index >= 0:
            if parser.done():
                self._concat(path, begin_index, len(path), lattice, parser)
            else:
                ss = path[-1].get_word_info().normalized_form
                if (parser.error_state == NumericParser.Error.COMMA and ss == ',') or \
                   (parser.error_state == NumericParser.Error.POINT and ss == '.'):
                    self._concat(path, begin_index, len(path) - 1, lattice, parser)

    def _concat(self, path, begin, end, lattice, parser) -> None:
        if path[begin].get_word_info().pos_id != self._numeric_pos_id:
            return
        if self._enable_normalize:
            normalized_form = parser.get_normalized()
            if end - begin > 1 or normalized_form != path[begin].get_word_info().normalized_form:
                self.concatenate(path, begin, end, lattice, normalized_form)
            return
        if end - begin > 1:
            self.concatenate(path, begin, end, lattice, '')
