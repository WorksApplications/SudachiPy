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


class BitVector(object):
    def __init__(self):
        self.UNIT_SIZE = 32
        self.units = []
        self.ranks = []
        self.num_ones = 0
        self.size = 0

    def get(self, id_):
        return (self.units[int(id_ / self.UNIT_SIZE)] >> (id_ % self.UNIT_SIZE) & 1) is 1

    def rank(self, id_):
        unit_id = int(id_ / self.UNIT_SIZE)
        return self.ranks[unit_id] \
            + self.pop_count(self.units[unit_id] & (~0 >> (self.UNIT_SIZE - (id_ % self.UNIT_SIZE) - 1)))

    def set_(self, id_, bit):
        if bit:
            self.units[int(id_ / self.UNIT_SIZE)] \
                = self.units[int(id_ / self.UNIT_SIZE)] | 1 << (id_ % self.UNIT_SIZE)
        else:
            self.units[int(id_ / self.UNIT_SIZE)] \
                = self.units[int(id_ / self.UNIT_SIZE)] & ~(1 << (id_ % self.UNIT_SIZE))

    def is_empty(self):
        return len(self.units) is 0

    def get_num_ones(self):
        return self.num_ones

    def get_size(self):
        return self.size

    def append(self):
        if (self.size % self.UNIT_SIZE) is 0:
            self.units.append(0)
        self.size += 1

    def build(self):
        self.ranks = [0] * len(self.units)
        self.num_ones = 0
        for i in range(len(self.units)):
            self.ranks[i] = self.num_ones
            self.num_ones += self.pop_count(self.units[i])

    def clear(self):
        self.units.clear()
        self.ranks = None

    def pop_count(self, unit):
        unit = ((unit & 0xAAAAAAAA) >> 1) + (unit & 0x55555555)
        unit = ((unit & 0xCCCCCCCC) >> 2) + (unit & 0x33333333)
        unit = ((unit >> 4) + unit) & 0x0F0F0F0F
        unit += unit >> 8
        unit += unit >> 16
        return unit & 0xFF
