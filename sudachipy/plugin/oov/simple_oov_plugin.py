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

from sudachipy.dictionarylib import wordinfo

from . import OovProviderPlugin


class SimpleOovPlugin(OovProviderPlugin):

    def __init__(self, json_obj):
        self.left_id = json_obj['leftId']
        self.right_id = json_obj['rightId']
        self.cost = json_obj['cost']
        self.__oov_pos_strings = json_obj['oovPOS']
        self.oov_pos_id = -1

    def set_up(self, grammar):
        self.oov_pos_id = grammar.get_part_of_speech_id(self.__oov_pos_strings)

    def provide_oov(self, input_text, offset, has_other_words):
        if not has_other_words:
            node = self.create_node()
            node.set_parameter(self.left_id, self.right_id, self.cost)
            length = input_text.get_word_candidate_length(offset)
            s = input_text.get_substring(offset, offset + length)
            info = wordinfo.WordInfo(surface=s, head_word_length=length, pos_id=self.oov_pos_id, normalized_form=s,
                                     dictionary_form_word_id=-1, dictionary_form=s, reading_form="",
                                     a_unit_split=[], b_unit_split=[], word_structure=[])
            node.set_word_info(info)
            return [node]
        else:
            return []
