import re

from sortedcontainers import SortedDict

from sudachipy.dictionarylib.wordinfo import WordInfo


class DictionaryBuilder(object):

    __MAX_LENGTH = 255
    __COLS_NUM = 18
    __BUFFER_SIZE = 1024 * 1024
    __PATTERN_UNICODE_LITERAL = re.compile(r"\\u([0-9a-fA-F]{4}|{[0-9a-fA-F]+})")
    __ARRAY_MAX_LENGTH = 127  # max value of byte in Java
    __STRING_MAX_LENGTH = 32767  # max value of short in Java

    class WordEntry:
        headword = None
        parameters = None
        wordinfo = None
        aunit_split_string = None
        bunit_split_string = None
        cunit_split_string = None

    class PosTable(object):

        def __init__(self):
            self.table = []

        def get_id(self, str_):
            id_ = self.table.index(str_) if str_ in self.table else -1
            if id_ < 0:
                id_ = len(self.table)
                self.table.append(str_)
            return id_

        def get_list(self):
            return self.table

    def __init__(self):
        self.buffer = bytearray(self.__BUFFER_SIZE)
        self.trie_keys = SortedDict()
        self.entries = []
        self.is_dictionary = False
        self.pos_table = self.PosTable()

    def is_length_valid(self, cols):
        head_length = len(cols[0].encode('utf-8'))
        return head_length <= self.__STRING_MAX_LENGTH \
            and len(cols[4]) <= self.__STRING_MAX_LENGTH \
            and len(cols[11]) <= self.__STRING_MAX_LENGTH \
            and len(cols[12]) <= self.__STRING_MAX_LENGTH

    def parse_line(self, cols):
        if len(cols) != self.__COLS_NUM:
            raise ValueError('invalid format')
        cols = [self.decode(col) for col in cols]
        if not self.is_length_valid(cols):
            raise ValueError('string is too long')
        if not cols[0]:
            raise ValueError('headword is empty')

        entry = self.WordEntry()
        # head word for trie
        if cols[1] != '-1':
            entry.headword = cols[0]
        # left-id, right-id, cost
        entry.parameters = [int(cols[i]) for i in [1, 2, 3]]
        # part of speech
        pos_id = self.get_posid(*cols[5:11])
        if pos_id < 0:
            raise ValueError('invalid part of speech')

        entry.aunit_split_string = cols[15]
        entry.bunit_split_string = cols[16]
        entry.cunit_split_string = cols[17]
        self.check_splitinfo_format(entry.aunit_split_string)
        self.check_splitinfo_format(entry.bunit_split_string)
        self.check_splitinfo_format(entry.cunit_split_string)

        if cols[14] == 'A' and \
                not (entry.aunit_split_string == '*' and entry.bunit_split_string == '*'):
            raise ValueError('invalid splitting')

        head_length = len(cols[0].encode('utf-8'))
        dict_from_wordid = -1 if cols[13] == '*' else int(cols[13])
        entry.wordinfo = WordInfo(
            cols[4], head_length, pos_id, cols[12], dict_from_wordid, '', cols[11], None, None, None)
        return entry

    def add_to_trie(self, headword, word_id):
        key = headword.encode('utf-8')
        if key not in self.trie_keys:
            self.trie_keys[key] = []
        self.trie_keys[key].append(word_id)

    def build(self):
        pass

    def build_lexicon(self):
        pass

    def get_posid(self, *strs):
        return self.pos_table.get_id(','.join(strs))

    def check_splitinfo_format(self, str_):
        if str_.count('/') + 1 > self.__ARRAY_MAX_LENGTH:
            raise ValueError('too many units')

    def write_grammar(self):
        pass

    def write_lexicon(self):
        pass

    def write_wordinfo(self):
        pass

    def decode(self, str_):
        def replace(match):
            uni_text = match.group()
            uni_text = uni_text.replace('{', '')
            uni_text = uni_text.replace('}', '')
            uni_text = uni_text.encode('ascii').decode('unicode-escape')
            return str(ord(uni_text))
        return re.sub(self.__PATTERN_UNICODE_LITERAL, replace, str_)

    def parse_splitinfo(self):
        pass

    def write_string(self):
        pass

    def write_int_array(self):
        pass
