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


class KeySet(object):
    def __init__(self, keys, values):
        self.keys = keys
        self.values = values

    def size(self):
        return len(self.keys)

    def get_key(self, id):
        return self.keys[id]

    def get_key_byte(self, key_id, byte_id):
        if byte_id >= len(self.keys[key_id]):
            return 0
        return self.keys[key_id][byte_id]

    def has_values(self):
        return self.values is not None

    def get_value(self, id):
        return self.values[id] if self.has_values() else id
