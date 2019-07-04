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
            node.begin = offset
            node.end = offset + node.get_word_info().length()
        return nodes

    @staticmethod
    def create_node() -> LatticeNode:
        node = LatticeNode()
        node.set_oov()
        return node
