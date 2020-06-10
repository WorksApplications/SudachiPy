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

from abc import ABC, abstractmethod
from typing import List

from sudachipy.dictionarylib.grammar import Grammar
from sudachipy.latticenode import LatticeNode
from sudachipy.utf8inputtext import UTF8InputText


class OovProviderPlugin(ABC):

    @abstractmethod
    def set_up(self, grammar: Grammar) -> None:
        raise NotImplementedError

    @abstractmethod
    def provide_oov(self, input_text: UTF8InputText, offset: int, has_other_words: bool) -> List[LatticeNode]:
        raise NotImplementedError

    def get_oov(self, input_text: UTF8InputText, offset: int, has_other_words: bool) -> List[LatticeNode]:
        nodes = self.provide_oov(input_text, offset, has_other_words)
        for node in nodes:
            node.set_begin(offset)
            node.set_end(offset + node.get_word_info().length())
        return nodes

    @staticmethod
    def create_node() -> LatticeNode:
        node = LatticeNode()
        node.set_oov()
        return node
