from sudachipy import config
from sudachipy.dictionarylib.grammar import Grammar

from .editconnectioncost import EditConnectionCostPlugin


class InhibitConnectionPlugin(EditConnectionCostPlugin):

    def __init__(self):
        self.inhibit_pairs = []

    def set_up(self, grammar: Grammar):
        self.inhibit_pairs = config.settings['inhibitedPair']

    def edit(self, grammar: Grammar):
        for pair in self.inhibit_pairs:
            if len(pair) < 2:
                continue
            self.inhibit_connection(grammar, pair[0], pair[1])
