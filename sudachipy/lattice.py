from typing import List, Optional

from .dictionarylib.grammar import Grammar
from .latticenode import LatticeNode


class Lattice:

    size = 0
    capacity = 0
    eos_node = None

    def __init__(self, grammar: Grammar):
        self.end_lists = []
        self.grammar = grammar
        self.eos_params = grammar.get_eos_parameter()
        bos_node = LatticeNode()
        bos_params = grammar.get_bos_parameter()
        bos_node.set_parameter(bos_params[0], bos_params[1], bos_params[2])
        bos_node.is_connected_to_bos = True
        self.end_lists.append([bos_node])

    def resize(self, size: int) -> None:
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

    def insert(self, begin: int, end: int, node: LatticeNode) -> None:
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
        return len(self.end_lists[index]) != 0

    def connect_node(self, r_node: LatticeNode) -> None:
        begin = r_node.begin
        r_node.total_cost = float('inf')
        for l_node in self.end_lists[begin]:
            if not l_node.is_connected_to_bos:
                continue
            # right_id and left_id look reversed, but it works ...
            connect_cost = self.grammar.get_connect_cost(l_node.right_id, r_node.left_id)
            if connect_cost == Grammar.INHIBITED_CONNECTION:
                continue
            cost = l_node.total_cost + connect_cost
            if cost < r_node.total_cost:
                r_node.total_cost = cost
                r_node.best_previous_node = l_node

        r_node.is_connected_to_bos = r_node.best_previous_node is not None
        r_node.total_cost += r_node.cost

    def connect_eos_node(self) -> None:
        self.connect_node(self.eos_node)

    def get_best_path(self) -> List[LatticeNode]:
        # self.connect_node(self.eos_node)
        if not self.eos_node.is_connected_to_bos:    # EOS node
            raise AttributeError("EOS is not connected to BOS")
        result = []
        node = self.eos_node
        while node is not self.end_lists[0][0]:
            result.append(node)
            node = node.best_previous_node
        return list(reversed(result))

    def dump(self, output):
        index = 0
        for i in range(self.size + 1, -1, -1):
            r_nodes = self.end_lists[i] if i <= self.size else [self.eos_node]
            for r_node in r_nodes:
                print("{}: {}: ".format(index, r_node), end="")
                index += 1
                for l_node in self.end_lists[r_node.begin]:
                    cost = l_node.total_cost + \
                        self.grammar.get_connect_cost(l_node.right_id, r_node.left_id)
                    print("{} ".format(cost), file=output, end="")
                print(file=output)
