import mmap
import os.path

from . import tokenizer
from . import config
from . import dictionarylib


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
        """

        self.input_text_plugins = settings["inputTextPlugin"]
        for p in self.input_text_plugins:
            p.set_up()
        self.oov_provider_plugins = settings["oovProviderPlugin"]
        if len(self.oov_provider_plugins) is 0:
            raise AttributeError("no OOV provider")
        for p in self.oov_provider_plugins:
            p.set_up(self.grammar)
        self.path_rewrite_plugins = os.path.join(config.RESOURCEDIR, settings["pathRewritePlugin"])
        for p in self.path_rewrite_plugins:
            p.set_up(self.grammar)

        for filename in os.path.join(config.RESOURCEDIR, settings["userDict"]):
            self.read_user_dictionary(filename)
        """

    def read_system_dictionary(self, filename):
        if filename is None:
            raise AttributeError("system dictionary is not specified")
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        self.buffers.append(bytes_)

        # grammar = dictionarylib.grammarimpl.GrammarImpl(bytes_, 0)
        offset = 0;
        header_storageSize = 8 + 8 + 256;
        offset += header_storageSize;
        grammar = dictionarylib.grammarimpl.GrammarImpl(bytes_, offset)
        self.grammar = grammar
        offset += grammar.get_storage_size()
        self.lexicon = dictionarylib.lexiconset.LexiconSet(dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, offset))

    def read_user_dictionary(self, filename):
        with open(filename, 'r+b') as user_dic:
            bytes_ = mmap.mmap(user_dic.fileno(), 0, prot=mmap.PROT_READ)
        self.buffers.append(bytes_)

        user_lexicon = dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, 0)
        tokenizer = tokenizer.JapaneseTokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, [])
        user_lexicon.calclate_cost(tokenizer)
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
