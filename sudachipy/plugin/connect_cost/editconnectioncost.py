from abc import ABC, abstractmethod

from sudachipy.dictionarylib.grammar import Grammar


class EditConnectionCostPlugin(ABC):

    @abstractmethod
    def set_up(self, grammar: Grammar) -> None:
        raise NotImplementedError

    @abstractmethod
    def edit(self, grammar: Grammar) -> None:
        raise NotImplementedError

    @staticmethod
    def inhibit_connection(grammar: Grammar, left_id: int, right_id: int) -> None:
        grammar.set_connect_cost(left_id, right_id, Grammar.INHIBITED_CONNECTION)
