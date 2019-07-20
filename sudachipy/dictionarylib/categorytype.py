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

from enum import Enum


class CategoryType(Enum):
    DEFAULT = 1
    SPACE = 1 << 1
    KANJI = 1 << 2
    SYMBOL = 1 << 3
    NUMERIC = 1 << 4
    ALPHA = 1 << 5
    HIRAGANA = 1 << 6
    KATAKANA = 1 << 7
    KANJINUMERIC = 1 << 8
    GREEK = 1 << 9
    CYRILLIC = 1 << 10
    USER1 = 1 << 11
    USER2 = 1 << 12
    USER3 = 1 << 13
    USER4 = 1 << 14
    NOOOVBOW = 1 << 15

    def get_id(self):
        return self.id

    def get_type(self, id_):
        for type_ in CategoryType.values():
            if type_.get_id() is id_:
                return type_
        return None

    @staticmethod
    def get(str_):
        try:
            return CategoryType[str_]
        except KeyError:
            return None
