from sudachipy.dictionarylib.categorytype import CategoryType

from .numericparser import NumericParser
from .path_rewrite_plugin import PathRewritePlugin


class JoinNumericPlugin(PathRewritePlugin):

    _numeric_pos_id = None

    def __init__(self, json_obj):
        if 'joinKanjiNumeric' in json_obj:
            pass  # Todo warn
        if 'enableNormalize' in json_obj:
            self._enable_normalize = json_obj['enableNormalize']
        self._NUMERIC_POS = ['名詞', '数詞', '*', '*', '*', '*']

    def set_up(self, grammar):
        self._numeric_pos_id = grammar.get_part_of_speech_id(self._NUMERIC_POS)

    def rewrite(self, text, path, lattice):
        begin_index = -1
        comma_as_digit = True
        period_as_digit = True
        parser = NumericParser()

        i = -1
        while i < len(path) - 1:
            i += 1
            node = path[i]
            types = self.get_char_category_types(text, node)
            s = node.get_word_info().normalized_form
            if CategoryType.NUMERIC in types or CategoryType.KANJINUMERIC in types or \
               (period_as_digit and s == '.') or (comma_as_digit and s == ','):

                if begin_index < 0:
                    parser.clear()
                    begin_index = i

                for j in range(len(s)):
                    c = s[j]
                    if not parser.append(c):
                        if begin_index >= 0:
                            comma_as_digit = parser.error_state != NumericParser.Error.COMMA
                            period_as_digit = parser.error_state != NumericParser.Error.POINT
                            i = begin_index - 1
                            begin_index = -1
                        break
            else:
                if begin_index >= 0:
                    if parser.done():
                        self._concat(path, begin_index, len(path), lattice, parser)
                    else:
                        ss = path[-1].get_word_info().normalized_form
                        if parser.error_state == NumericParser.Error.COMMA and ss == ',' or \
                           parser.error_state == NumericParser.Error.POINT and ss == '.':
                            self._concat(path, begin_index, len(path) - 1, lattice, parser)
                            i = begin_index + 2
                begin_index = -1
                comma_as_digit = not comma_as_digit and s != ','
                period_as_digit = not period_as_digit and s != '.'

            if begin_index >= 0:
                if parser.done():
                    self._concat(path, begin_index, len(path), lattice, parser)
                else:
                    ss = path[-1].get_word_info().normalized_form
                    if parser.error_state == NumericParser.Error.COMMA and ss == ',' or \
                       parser.error_state == NumericParser.Error.POINT and ss == '.':
                        self._concat(path, begin_index, len(path) - 1, lattice, parser)

    def _concat(self, path, begin, end, lattice, parser) -> None:
        if path[begin].get_word_info().pos_id != self._numeric_pos_id:
            return
        if self._enable_normalize:
            normalized_form = parser.get_normalized()
            if end - begin < 1 or not normalized_form == path[begin].get_word_info.normalized_form:
                self.concatenate(path, begin, end, lattice, normalized_form)
            elif end - begin > 1:
                self.concatenate(path, begin, end, lattice, None)
