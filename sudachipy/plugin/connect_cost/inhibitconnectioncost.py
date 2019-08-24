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

from sudachipy import config
from sudachipy.dictionarylib.grammar import Grammar

from .editconnectioncost import EditConnectionCostPlugin


class InhibitConnectionPlugin(EditConnectionCostPlugin):
    """ A Edit Connection Cost Plugin for inhibiting the connections.

    The following is an example of settings.

    ``
    {
        {
            "class" : "sudachipy.plugin.connect_cost.InhibitConnectionPlugin",
            "inhibitedPair" : [ [ 0, 233 ], [435, 332] ]
        }
    }
    ``

    Attributes:
        _inhibit_pairs: a list of int pairs. At each pair, the first one is right-ID
        of the left node and the second one is left-ID of the right node in a connection.

    """

    def __init__(self):
        self._inhibit_pairs = []

    def set_up(self, grammar: Grammar) -> None:
        if 'inhibitedPair' in config.settings:
            self._inhibit_pairs = config.settings['inhibitedPair']

    def edit(self, grammar: Grammar) -> None:
        for pair in self._inhibit_pairs:
            if len(pair) < 2:
                continue
            self.inhibit_connection(grammar, pair[0], pair[1])
