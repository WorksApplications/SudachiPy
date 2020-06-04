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

from typing import List, Optional

from .dictionarylib.grammar import Grammar
from .latticenode cimport LatticeNode

cdef class Lattice:

    def __init__(self, grammar: Grammar):
        self.size = 0
        self.capacity = 0


        self.end_lists = []
        self.grammar = grammar
        self.eos_params = grammar.get_eos_parameter()
        cdef LatticeNode bos_node = LatticeNode()
        bos_params = grammar.get_bos_parameter()
        bos_node.set_parameter(bos_params[0], bos_params[1], bos_params[2])
        bos_node.is_connected_to_bos = True
        self.end_lists.append([bos_node])
        self.connect_costs = self.grammar._matrix_view

    cpdef void resize(self, int size):
        if size > self.capacity:
            self.expand(size)
        self.size = size
        self.eos_node = LatticeNode()
        self.eos_node.set_parameter(self.eos_params[0], self.eos_params[1], self.eos_params[2])
        self.eos_node.begin = self.eos_node.end = size

    def clear(self) -> None:
        for i in range(1, self.size + 1):
            self.end_lists[i].clear()
        self.size = 0
        self.eos_node = None

    def expand(self, new_size: int) -> None:
        expand_list = [[] for _ in range(self.size, new_size)]
        self.end_lists.extend(expand_list)
        self.capacity = new_size

    def get_nodes_with_end(self, end: int) -> List[LatticeNode]:
        return self.end_lists[end]

    def get_nodes(self, begin: int, end: int) -> List[LatticeNode]:
        return [node for node in self.end_lists[end] if node.begin == begin]

    def get_minumum_node(self, begin: int, end: int) -> Optional[LatticeNode]:
        nodes = self.get_nodes(begin, end)
        if not nodes:
            return None
        min_arg = nodes[0]
        for node in nodes[1:]:
            if node.cost < min_arg.cost:
                min_arg = node
        return min_arg

    cpdef void insert(self, int begin, int end, LatticeNode node):
        self.end_lists[end].append(node)
        node.begin = begin
        node.end = end
        self.connect_node(node)

    def remove(self, begin: int, end: int, node: LatticeNode) -> None:
        self.end_lists[end].remove(node)

    @staticmethod
    def create_node() -> LatticeNode:
        return LatticeNode()

    def has_previous_node(self, index: int) -> bool:
        return bool(self.end_lists[index])

    cdef void connect_node(self, LatticeNode r_node):
        begin = r_node.begin
        r_node.total_cost = INT_MAX

        cdef LatticeNode l_node
        cdef int connect_cost
        for l_node in self.end_lists[begin]:
            if not l_node.is_connected_to_bos:
                continue
            # right_id and left_id look reversed, but it works ...
            connect_cost = self.connect_costs[l_node.right_id, r_node.left_id]

            # 0x7fff == Grammar.INHIBITED_CONNECTION:
            if connect_cost == 0x7fff:
                continue
            cost = l_node.total_cost + connect_cost
            if cost < r_node.total_cost:
                r_node.total_cost = cost
                r_node.best_previous_node = l_node

        r_node.is_connected_to_bos = r_node.best_previous_node is not None
        r_node.total_cost += r_node.cost

    cdef void connect_eos_node(self):
        self.connect_node(self.eos_node)

    def get_best_path(self) -> List[LatticeNode]:
        # self.connect_node(self.eos_node)
        if not self.eos_node.is_connected_to_bos:    # EOS node
            raise AttributeError("EOS is not connected to BOS")
        result = []
        node = self.eos_node.best_previous_node
        while node is not self.end_lists[0][0]:
            result.append(node)
            node = node.best_previous_node
        return list(reversed(result))

    def dump(self, logger):
        if logger.disabled:
            return
        index = 0
        for i in range(self.size + 1, -1, -1):
            r_nodes = self.end_lists[i] if i <= self.size else [self.eos_node]
            for r_node in r_nodes:
                surface = '(null)'
                pos = 'BOS/EOS'
                if r_node.is_defined:
                    wi = r_node.get_word_info()
                    surface = wi.surface
                    pos_id = wi.pos_id
                    pos = '(null)'
                    if pos_id >= 0:
                        pos = ','.join(self.grammar.get_part_of_speech_string(pos_id))

                costs = []
                for l_node in self.end_lists[r_node.begin]:
                    cost = self.grammar.get_connect_cost(l_node.right_id, r_node.left_id)
                    costs.append(str(cost))
                index += 1

                logger.info('%d: %d %d %s(%d) %s %d %d %d: %s' %
                            (index, r_node.get_begin(), r_node.get_end(),
                             surface, r_node.word_id, pos, r_node.left_id,
                             r_node.right_id, r_node.cost, ' '.join(costs)))
