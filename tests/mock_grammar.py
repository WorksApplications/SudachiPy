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
from unittest import mock

from sudachipy.dictionarylib.charactercategory import CharacterCategory
from sudachipy.dictionarylib.grammar import Grammar

mocked_grammar = mock.Mock(spec=Grammar)
mocked_grammar.get_part_of_speech_size.return_value = 0
mocked_grammar.get_part_of_speech_string.return_value = None
mocked_grammar.get_part_of_speech_id.return_value = 0
mocked_grammar.get_connect_cost.return_value = 0
# mocked_grammar.set_connect_cost.return_value = None
mocked_grammar.get_bos_parameter.return_value = None
mocked_grammar.get_eos_parameter.return_value = None


def mocked_get_character_category():
    cat = CharacterCategory()
    test_resources_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        os.pardir,
        'sudachipy',
        'resources')
    try:
        cat.read_character_definition(os.path.join(test_resources_dir, 'char.def'))
    except IOError as e:
        print(e)
    return cat


mocked_grammar.get_character_category.side_effect = mocked_get_character_category


mocked_grammar.set_character_category.return_value = None
