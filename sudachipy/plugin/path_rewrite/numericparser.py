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
from io import StringIO


class NumericParser(object):

    class StringNumber(object):

        def __init__(self):
            self._significand = StringIO()
            self._scale = 0
            self._point = -1
            self._is_all_zero = True

        def clear(self) -> None:
            self._significand.seek(0)
            self._significand.truncate(0)
            self._scale = 0
            self._point = -1
            self._is_all_zero = True

        def append(self, i: int) -> None:
            if i != 0:
                self._is_all_zero = False
            self._significand.write(str(i))

        def shift_scale(self, i: int) -> None:
            if self.is_zero():
                self._significand.write('1')
            self._scale += i

        def add(self, number: 'StringNumber') -> bool:  # noqa: F821
            if number.is_zero():
                return True

            if self.is_zero():
                self._significand.write(number.significand_value())
                self._scale = number.scale
                self._point = number.point
                return True

            self.normalize_scale()
            length = number.int_length()
            if self._scale >= length:
                self.fill_zero(self._scale - length)
                if number.point >= 0:
                    self._point = self._significand.tell() + number.point
                self._significand.write(number.significand_value())
                self._scale = number.scale
                return True

            return False

        def set_point(self) -> bool:
            if self._scale == 0 and self._point < 0:
                self._point = self._significand.tell()
                return True
            return False

        def int_length(self) -> int:
            self.normalize_scale()
            if self._point >= 0:
                return self._point
            return self._significand.tell() + self._scale

        def is_zero(self):
            return self._significand.tell() == 0

        def normalize_scale(self) -> None:
            if self._point < 0:
                return
            n_scale = self._significand.tell() - self._point
            if n_scale > self._scale:
                self._point += self._scale
                self._scale = 0
            else:
                self._scale -= n_scale
                self._point = -1

        def fill_zero(self, length: int) -> None:
            if length > 0:
                self._significand.write('0' * length)

        @property
        def scale(self) -> int:
            return self._scale

        @property
        def point(self) -> int:
            return self._point

        @property
        def is_all_zero(self) -> bool:
            return self._is_all_zero

        def significand_value(self) -> str:
            return self._significand.getvalue()

        def insert_significand(self, idx: int, text: str) -> None:
            self._significand.seek(idx)
            post_fix = self._significand.read()
            self._significand.seek(idx)
            self._significand.write(text)
            self._significand.write(post_fix)

        def __str__(self):
            if self.is_zero():
                return '0'

            self.normalize_scale()
            if self._scale > 0:
                self.fill_zero(self._scale)
            elif self._point >= 0:
                self.insert_significand(self._point, '.')
                if self._point == 0:
                    self.insert_significand(0, '0')
                i = self._significand.tell() - 1
                self._significand.seek(i)
                while i >= 0 and self._significand.read(1) == '0':
                    i -= 1
                    self._significand.seek(i)
                self._significand.truncate(i + 1)
                self._significand.seek(i)
                if self._significand.read(1) == '.':
                    self._significand.truncate(i)

            return self._significand.getvalue()

    class Error(Enum):
        NONE = 1
        POINT = 2
        COMMA = 3
        OTHER = 4

    _digit_length = 0
    _is_first_digit = True
    _has_comma = False
    _has_hanging_point = False
    _error_state = Error.NONE
    _total = None
    _sub_total = None
    _tmp = None

    def __init__(self):
        self._char_to_num = {}
        for i in range(10):
            self._char_to_num[str(i)] = i
        self._char_to_num['〇'] = 0
        self._char_to_num['一'] = 1
        self._char_to_num['二'] = 2
        self._char_to_num['三'] = 3
        self._char_to_num['四'] = 4
        self._char_to_num['五'] = 5
        self._char_to_num['六'] = 6
        self._char_to_num['七'] = 7
        self._char_to_num['八'] = 8
        self._char_to_num['九'] = 9
        self._char_to_num['十'] = -1
        self._char_to_num['百'] = -2
        self._char_to_num['千'] = -3
        self._char_to_num['万'] = -4
        self._char_to_num['億'] = -8
        self._char_to_num['兆'] = -12

        self._total = self.StringNumber()
        self._sub_total = self.StringNumber()
        self._tmp = self.StringNumber()
        self.clear()

    def clear(self) -> None:
        self._digit_length = 0
        self._is_first_digit = True
        self._has_comma = False
        self._has_hanging_point = False
        self._error_state = self.Error.NONE
        self._total.clear()
        self._sub_total.clear()
        self._tmp.clear()

    def append(self, char: str) -> bool:
        if len(char) > 1:
            raise ValueError('char must be single character string')
        if char == '.':
            self._has_hanging_point = True
            if self._is_first_digit:
                self._error_state = self.Error.POINT
                return False
            if self._has_comma and not self.check_comma():
                self._error_state = self.Error.COMMA
                return False
            if not self._tmp.set_point():
                self._error_state = self.Error.POINT
                return False
            self._has_comma = False
            return True
        if char == ',':
            if not self.check_comma():
                self._error_state = self.Error.COMMA
                return False
            self._has_comma = True
            self._digit_length = 0
            return True

        if char not in self._char_to_num:
            return False

        num = self._char_to_num[char]
        if self.is_small_unit(num):
            self._tmp.shift_scale(-num)
            if not self._sub_total.add(self._tmp):
                return False
            self._tmp.clear()
            self._is_first_digit = True
            self._digit_length = 0
            self._has_comma = False
            return True
        if self.is_large_unit(num):
            if not self._sub_total.add(self._tmp) or self._sub_total.is_zero():
                return False
            self._sub_total.shift_scale(-num)
            if not self._total.add(self._sub_total):
                return False
            self._sub_total.clear()
            self._tmp.clear()
            self._is_first_digit = True
            self._digit_length = 0
            self._has_comma = False
            return True
        self._tmp.append(num)
        self._is_first_digit = False
        self._digit_length += 1
        self._has_hanging_point = False
        return True

    def done(self) -> bool:
        ret = self._sub_total.add(self._tmp) and self._total.add(self._sub_total)
        if self._has_hanging_point:
            self._error_state = self.Error.POINT
            return False
        if self._has_comma and self._digit_length != 3:
            self._error_state = self.Error.COMMA
            return False
        return ret

    def get_normalized(self) -> str:
        return str(self._total)

    def check_comma(self) -> bool:
        if self._is_first_digit:
            return False
        if not self._has_comma:
            return self._digit_length <= 3 and not self._tmp.is_zero() and not self._tmp.is_all_zero
        return self._digit_length == 3

    @staticmethod
    def is_small_unit(num: int):
        return -3 <= num < 0

    @staticmethod
    def is_large_unit(num: int):
        return num <= -4

    @property
    def error_state(self):
        return self._error_state
