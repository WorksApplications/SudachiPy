from abc import ABC, abstractmethod

from sudachipy.dictionarylib.grammar import Grammar


class EditConnectionCostPlugin(ABC):

    @abstractmethod
    def set_up(self, grammar: Grammar):
        raise NotImplementedError

    @abstractmethod
    def edit(self, grammar: Grammar):
        raise NotImplementedError

    @staticmethod
    def inhibit_connection(grammar: Grammar, left_id: int, right_id: int):
        grammar.set_connect_cost(left_id, right_id, Grammar.INHIBITED_CONNECTION)
