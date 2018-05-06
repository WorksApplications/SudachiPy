import mmap
import os.path

from sudachipy import config
from sudachipy import dictionarylib
from sudachipy import tokenizer
from sudachipy import plugin


class Dictionary:
    def __init__(self, settings, path=None):
        self.grammar = None
        self.lexicon = None
        self.input_text_plugins = []
        self.oov_provider_plugins = []
        self.path_rewrite_plugins = []
        self.buffers = []

        if path is None:
            pass

        self.buffers = []

        self.read_system_dictionary(os.path.join(config.RESOURCEDIR, settings["systemDict"]))
        """
        for p in settings["editConnectionPlugin"]:
            p.set_up(self.grammar)
            p.edit(self.grammar)
        """

        self.read_character_definition(os.path.join(config.RESOURCEDIR, settings["characterDefinitionFile"]))

        default_input_text_plugin = plugin.default_input_text_plugin.DefaultInputTextPlugin()
        self.input_text_plugins = [default_input_text_plugin]
        for p in self.input_text_plugins:
            p.set_up()

        simple_oov_plugin = plugin.simple_oov_plugin.SimpleOovPlugin()
        mecab_oov_plugin = plugin.mecab_oov_plugin.MeCabOovPlugin()
        self.oov_provider_plugins = [mecab_oov_plugin, simple_oov_plugin]
        if not self.oov_provider_plugins:
            raise AttributeError("no OOV provider")
        for p in self.oov_provider_plugins:
            p.set_up(self.grammar)

        join_numeric_plugin = plugin.join_numeric_plugin.JoinNumericPlugin()
        join_katakana_oov_plugin = plugin.join_katakana_oov_plugin.JoinKatakanaOovPlugin()
        self.path_rewrite_plugins = [join_numeric_plugin, join_katakana_oov_plugin]
        for p in self.path_rewrite_plugins:
            p.set_up(self.grammar)

        """
        for filename in os.path.join(config.RESOURCEDIR, settings["userDict"]):
            self.read_user_dictionary(filename)
        """

    def read_system_dictionary(self, filename):
        if filename is None:
            raise AttributeError("system dictionary is not specified")
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        self.buffers.append(bytes_)

        offset = 0
        self.header = dictionarylib.dictionaryheader.DictionaryHeader(bytes_, offset)
        SYSTEM_DICT_VERSION = 0x7366d3f18bd111e7
        if self.header.version != SYSTEM_DICT_VERSION:
            raise Exception("invalid system dictionary")
        offset += self.header.storage_size

        self.grammar = dictionarylib.grammar.Grammar(bytes_, offset)
        offset += self.grammar.get_storage_size()

        self.lexicon = dictionarylib.lexiconset.LexiconSet(dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, offset))

    def read_user_dictionary(self, filename):
        with open(filename, 'r+b') as user_dic:
            bytes_ = mmap.mmap(user_dic.fileno(), 0, prot=mmap.PROT_READ)
        self.buffers.append(bytes_)

        user_lexicon = dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, 0)
        tokenizer_obj = tokenizer.Tokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, [])
        user_lexicon.calclate_cost(tokenizer_obj)
        self.lexicon.append(user_lexicon)

    def read_character_definition(self, filename):
        if self.grammar is None:
            return
        char_category = dictionarylib.charactercategory.CharacterCategory()
        char_category.read_character_definition(filename)
        self.grammar.set_character_category(char_category)

    def close(self):
        self.grammar = None
        self.lexicon = None
        for buffer_ in self.buffers:
            buffer_.close()

    def create(self):
        return tokenizer.Tokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, self.path_rewrite_plugins)
