import re
from io import BytesIO
from logging import DEBUG, StreamHandler, getLogger

from sortedcontainers import SortedDict

from sudachipy.dictionarylib.wordinfo import WordInfo


class DictionaryBuilder(object):

    __BYTE_MAX_VALUE = 127
    __MAX_LENGTH = 255
    __COLS_NUM = 18
    __BUFFER_SIZE = 1024 * 1024
    __PATTERN_UNICODE_LITERAL = re.compile(r"\\u([0-9a-fA-F]{4}|{[0-9a-fA-F]+})")
    __ARRAY_MAX_LENGTH = __BYTE_MAX_VALUE  # max value of byte in Java
    __STRING_MAX_LENGTH = 32767  # max value of short in Java
    is_user_dictionary = False

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

    @staticmethod
    def __default_logger():
        handler = StreamHandler()
        handler.setLevel(DEBUG)
        logger = getLogger(__name__)
        logger.setLevel(DEBUG)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    def __init__(self, *, logger=None):
        self.buffer = BytesIO()
        self.trie_keys = SortedDict()
        self.entries = []
        self.is_dictionary = False
        self.pos_table = self.PosTable()
        self.logger = logger or self.__default_logger()

    def build(self, lexicon_paths, file_in, file_out):
        pass

    def build_lexicon(self, filename, io_in):
        pass

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

    def is_length_valid(self, cols):
        head_length = len(cols[0].encode('utf-8'))
        return head_length <= self.__STRING_MAX_LENGTH \
            and len(cols[4]) <= self.__STRING_MAX_LENGTH \
            and len(cols[11]) <= self.__STRING_MAX_LENGTH \
            and len(cols[12]) <= self.__STRING_MAX_LENGTH

    def add_to_trie(self, headword, word_id):
        key = headword.encode('utf-8')
        if key not in self.trie_keys:
            self.trie_keys[key] = []
        self.trie_keys[key].append(word_id)

    def get_posid(self, *strs):
        return self.pos_table.get_id(','.join(strs))

    def write_grammar(self):
        pass

    def convert_postable(self, pos_list):
        self.buffer.write(len(pos_list).to_bytes(2, byteorder='little'))
        for pos in pos_list:
            for text in pos.split(','):
                self.write_string(text)

    def convert_matrix(self, matrix_in):
        pass

    def write_lexicon(self):
        pass

    def write_wordinfo(self, io_out):
        pass

    def decode(self, str_):
        def replace(match):
            uni_text = match.group()
            uni_text = uni_text.replace('{', '').replace('}', '')
            if len(uni_text) > 6:
                uni_text = ('\\U000{}'.format(uni_text[2:]))
            return uni_text.encode('ascii').decode('unicode-escape')
        return re.sub(self.__PATTERN_UNICODE_LITERAL, replace, str_)

    def check_splitinfo_format(self, str_):
        if str_.count('/') + 1 > self.__ARRAY_MAX_LENGTH:
            raise ValueError('too many units')

    def parse_splitinfo(self, info):
        if info == '*':
            return []
        words = info.split('/')
        if len(words) > self.__ARRAY_MAX_LENGTH:
            raise ValueError('too many units')
        ids = []
        for word in words:
            if self.is_id(word):
                ids.append(self.parse_id(word))
            else:
                ids.append(self.word_to_id(word))
                if ids[-1] < 0:
                    return ValueError('not found such a word')
        return ids

    def is_id(self, text):
        return re.match(r'U?\d+', text)

    def parse_id(self, text):
        if text.startswith('U'):
            id_ = int(text[1:])
            if self.is_user_dictionary:
                id_ |= (1 << 28)
        else:
            id_ = int(text)
        self.check_wordid(id_)
        return id_

    def word_to_id(self, text):
        cols = text.split(',')
        if len(cols) < 8:
            raise ValueError('too few columns')
        headword = self.decode(cols[0])
        pos_id = self.get_posid([cols[i] for i in range(1, 7)])
        if pos_id < 0:
            raise ValueError('invalid part of speech')
        reading = self.decode(cols[7])
        return self.get_wordid(headword, pos_id, reading)

    def get_wordid(self, headword, pos_id, reading_form):
        for i in range(len(self.entries)):
            info = self.entries[i].wordinfo
            if info.surface == headword \
                    and info.pos_id == pos_id \
                    and info.reading_form == reading_form:
                return i
        return -1

    def check_wordid(self, wid):
        if wid < 0 or wid >= len(self.entries):
            raise ValueError('invalid word ID')

    def write_string(self, text):
        len_ = 0
        for c in text:
            if 0x10000 <= ord(c) <= 0x10FFFF:
                len_ += 2
            else:
                len_ += 1
        self.write_stringlength(len_)
        self.buffer.write(text.encode('utf-16-le'))

    def write_stringlength(self, len_):
        if len_ <= self.__BYTE_MAX_VALUE:
            self.buffer.write(len_.to_bytes(1, byteorder='little'))
        else:
            self.buffer.write(
                ((len_ >> 8) | 0x80).to_bytes(1, byteorder='little'))
            self.buffer.write(
                (len_ & 0xFF).to_bytes(1, byteorder='little'))

    def write_intarray(self, array):
        self.buffer.write(len(array).to_bytes(1, byteorder='little'))
        for item in array:
            self.buffer.write(item.to_bytes(4, byteorder='little'))
