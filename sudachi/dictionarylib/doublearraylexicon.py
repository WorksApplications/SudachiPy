import itertool
from . import lexicon
from . import dartsclone
from . import wordidtable
from . import wordparameterlist
from . import wordinfolist


class DoubleArrayLexicon(lexicon.Lexicon):

    def __init__(self, bytes_, offset):
        self.trie = dartsclone.doublearray.DoubleArray()
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')
        offset += 4
        bytes_.seek(offset)
        self.trie.set_array(bytes_, self.size)
        offset += self.trie.total_size()

        self.word_id_table = wordidtable.WordIdTable(bytes_, offset)
        offset += self.word_id_table.storage_size()

        self.word_params = wordparameterlist.WordParameterList(bytes_, offset)
        offset += self.word_params.storage_size()

        self.word_infos = wordinfolist.WordInfoList(bytes_, offset, self.word_params.get_size())

    def lookup(self, text, offset):
        r = trie.common_prefix_search(text, offset)
        if len(r) is 0:
            return r
        lambda p: word_id_table[p[0]]
        return r.

    def get_left_id(self, word_id):
        pass

    def get_right_id(self, word_id):
        pass

    def get_cost(self, word_id):
        pass

    def get_word_info(self, word_id):
        pass
