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

import math
import re
from queue import PriorityQueue

from . import categorytype


class CharacterCategory(object):

    class Range(object):

        def __lt__(self, other):
            return self.high < other.high

        def __init__(self, low=0, high=0, categories=None):
            self.low = low
            self.high = high
            self.categories = categories or []

        def contains(self, cp):
            return self.low <= cp < self.high

        def containing_length(self, text):
            for i in range(len(text)):
                c = ord(text[i])
                if c < self.low or c > self.high:
                    return i
            return len(text)

        def lower(self, cp):
            return self.high <= cp

        def higher(self, cp):
            return self.low > cp

        def match(self, other):
            return self.low == other.low and self.high == other.high

    def __init__(self):
        self.range_list = []

    def _compile(self) -> None:
        """
        _compile transforms self.range_list to non overlapped range list
        to apply binary search in get_category_types
        :return:
        """
        self.range_list.sort(key=lambda x: x.high)
        self.range_list.sort(key=lambda x: x.low)
        new_range_list = []
        left_chain = PriorityQueue()
        right_chain = self.range_list
        states = []
        pivot = 0
        while True:
            if left_chain.empty():
                if not right_chain:
                    break
                right = right_chain.pop(0)
                left_chain.put(right)
                pivot = right.low
                states.extend(right.categories)
                continue
            left = left_chain.get()
            right = right_chain[0] if right_chain else None
            left_end = left.high
            right_begin = right.low if right else math.inf
            if left_end <= right_begin:
                new_range_list.append(self.Range(pivot, left_end, set(states)))
                pivot = left_end
                for cat in left.categories:
                    states.remove(cat)
                continue
            else:
                new_range_list.append(self.Range(pivot, right_begin, set(states)))
                pivot = right_begin
                states.extend(right.categories)
                left_chain.put(right)
                left_chain.put(left)
                right_chain.pop(0)
        self.range_list = []
        _range = new_range_list[0]
        for irange in new_range_list[1:]:
            if irange.low == _range.high and irange.categories == _range.categories:
                _range = self.Range(_range.low, irange.high, _range.categories)
            else:
                self.range_list.append(_range)
                _range = irange
        self.range_list.append(_range)

    def get_category_types(self, code_point):
        begin = 0
        n = len(self.range_list)
        end = n
        pivot = (begin + end) // 2
        while 0 <= pivot < n:
            range_ = self.range_list[pivot]
            if range_.contains(code_point):
                return range_.categories
            if range_.lower(code_point):
                begin = pivot
            else:  # range_.higher(code_point)
                end = pivot
            new_pivot = (begin + end) // 2
            if new_pivot == pivot:
                break
            pivot = new_pivot
        return {categorytype.CategoryType.DEFAULT}

    def read_character_definition(self, char_def=None):
        """
        :param char_def: path
        """

        if char_def is not None:
            f = open(char_def, 'r', encoding="utf-8")
        else:
            f = open("char.def", 'r', encoding="utf-8")

        for i, line in enumerate(f.readlines()):
            line = line.rstrip()
            if re.fullmatch(r"\s*", line) or re.match("#", line):
                continue
            cols = re.split(r"\s+", line)
            if len(cols) < 2:
                f.close()
                raise AttributeError("invalid format at line {}".format(i))
            if not re.match("0x", cols[0]):
                continue
            range_ = self.Range()
            r = re.split("\\.\\.", cols[0])
            range_.low = int(r[0], 16)
            range_.high = range_.low + 1
            if len(r) > 1:
                range_.high = int(r[1], 16) + 1
            if range_.low >= range_.high:
                f.close()
                raise AttributeError("invalid range at line {}".format(i))
            for j in range(1, len(cols)):
                if re.match("#", cols[j]) or cols[j] == '':
                    break
                type_ = categorytype.CategoryType.get(cols[j])
                if type_ is None:
                    f.close()
                    raise AttributeError("{} is invalid type at line {}".format(cols[j], i))
                range_.categories.append(type_)
            self.range_list.append(range_)

        f.close()
        self._compile()
