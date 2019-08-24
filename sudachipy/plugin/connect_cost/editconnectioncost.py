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

from sudachipy.dictionarylib.grammar import Grammar


class EditConnectionCostPlugin(ABC):
    """ Interface of plugins for editing the connection costs.

    The following is an example of settings.
    ``
    {
        {
            "class" : "sudachipy.plugin.connect_cost.SampleEditConnectionPlugin",
            "example" : "example setting"
        }
    }
    ``

    """

    @abstractmethod
    def set_up(self, grammar: Grammar) -> None:
        """ Set up plugin.

        Args:
            grammar: grammar of system dictionary

        """
        raise NotImplementedError

    @abstractmethod
    def edit(self, grammar: Grammar) -> None:
        """ Edit a connection costs.

        Args:
            grammar: grammar of system dictionary

        """
        raise NotImplementedError

    @staticmethod
    def inhibit_connection(grammar: Grammar, left: int, right: int) -> None:
        """ Inhibit a connection.

        Args:
            grammar: grammar of system dictionary
            left: right-ID of left node
            right: left-ID of right node

        """
        grammar.set_connect_cost(left, right, Grammar.INHIBITED_CONNECTION)
