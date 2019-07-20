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

from sudachipy.dictionarylib.categorytype import CategoryType
from sudachipy.latticenode import LatticeNode
from sudachipy.plugin.path_rewrite.path_rewrite_plugin import PathRewritePlugin
from sudachipy.utf8inputtext import UTF8InputText


class JoinKatakanaOovPlugin(PathRewritePlugin):

    def __init__(self, json_obj):
        self.__pos = json_obj['oovPOS']
        self._min_length = 1
        if 'minLength' in json_obj:
            self._min_length = json_obj['minLength']
        self.oov_pos_id = None

    def set_up(self, grammar):
        if not self.__pos:
            raise ValueError("oovPOS is undefined")
        self.oov_pos_id = grammar.get_part_of_speech_id(self.__pos)
        if self.oov_pos_id < 0:
            raise ValueError("oovPOS is invalid")

    def rewrite(self, text, path, lattice):
        i = 0
        while True:
            if i >= len(path):
                break
            node = path[i]
            if not (node.is_oov() or self.is_shorter(self._min_length, text, node)) or \
                    not self.is_katakana_node(text, node):
                i += 1
                continue
            begin = i - 1
            while True:
                if begin < 0:
                    break
                if not self.is_katakana_node(text, path[begin]):
                    begin += 1
                    break
                begin -= 1
            begin = max(0, begin)
            end = i + 1
            while True:
                if end >= len(path):
                    break
                if not self.is_katakana_node(text, path[end]):
                    break
                end += 1
            pass
            while begin != end and not self.can_oov_bow_node(text, path[begin]):
                begin += 1
            if (end - begin) > 1:
                self.concatenate_oov(path, begin, end, self.oov_pos_id, lattice)
                i = begin + 1  # skip next node, as we already know it is not a joinable katakana
            i += 1

    def is_katakana_node(self, text, node):
        return CategoryType.KATAKANA in self.get_char_category_types(text, node)

    def is_one_char(self, text, node):
        b = node.get_begin()
        return b + text.get_code_points_offset_length(b, 1) == node.get_end()

    def can_oov_bow_node(self, text, node):
        return CategoryType.NOOOVBOW not in text.get_char_category_types(node.get_begin())

    @staticmethod
    def is_shorter(length: int, text: UTF8InputText, node: LatticeNode):
        return text.code_point_count(node.begin, node.end) < length
