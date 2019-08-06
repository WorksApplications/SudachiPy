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

from enum import Flag, auto


class CategoryType(Flag):
    NONE = 0
    DEFAULT = auto()
    SPACE = auto()
    KANJI = auto()
    SYMBOL = auto()
    NUMERIC = auto()
    ALPHA = auto()
    HIRAGANA = auto()
    KATAKANA = auto()
    KANJINUMERIC = auto()
    GREEK = auto()
    CYRILLIC = auto()
    USER1 = auto()
    USER2 = auto()
    USER3 = auto()
    USER4 = auto()
    NOOOVBOW = auto()

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

    def type_wise(self):
        for type_ in CategoryType:
            value = self & type_
            if value == CategoryType.NONE:
                continue
            yield value
