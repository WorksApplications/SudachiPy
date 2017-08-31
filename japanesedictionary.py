import mmap

from . import dictionary
from . import japanesetokenizer
from . import settings
import dictionarylib


class JapaneseDictionary(dictionary.Dictionary):
    def __init__(self, json_string, path=None):
        self.grammar = None
        self.lexicon = None
        self.input_text_plugins = []
        self.oov_provider_plugins = []
        self.path_rewrite_plugins = []
        self.buffers = []

        if path is None:
            pass

        self.settings = settings.parse_settings(path, json_string)

        self.buffers = []

        self.read_system_dictionary(self.settings.get_path("system_dict"))
        for p in self.settings.get_plugin_list("edit_connection_plugin"):
            p.set_up(self.grammar)
            p.edit(self.grammar)

        self.read_caracter_definition(self.settings.get_path("character_definition_file"))

        self.input_text_plugins = self.settings.get_plugin_list("input_text_plugin")
        for p in self.input_text_plugins:
            p.set_up()
        self.oov_provider_plugins = self.settings.get_plugin_list("oov_provider_plugin")
        if len(self.oov_provider_plugins) is 0:
            raise AttributeError("no OOV provider")
        for p in self.oov_provider_plugins:
            p.set_up(self.grammar)
        self.path_rewrite_plugins = self.settings.get_plugin_list("path_rewrite_plugin")
        for p in self.path_rewrite_plugins:
            p.set_up(self.grammar)

        for filename in self.settings.get_path_list("user_dict"):
            self.read_user_dictionary(filename)

    def read_system_dictionary(self, filename):
        if filename is None:
            raise AttributeError("system dictionary is not specified")
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), prot=mmap.PROT_READ)
        self.buffers.append(bytes_)

        grammar = dictionarylib.grammarimpl.GrammarImpl(bytes_, 0)
        self.grammar = grammar
        self.lexicon = dictionarylib.lexiconset.LexiconSet(dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, grammar.storage_size()))

    def read_user_dictionary(self, filename):
        with open(filename, 'r+b') as user_dic:
            bytes_ = mmap.mmap(user_dic.fileno(), prot=mmap.PROT_READ)
        self.buffers.append(bytes_)

        user_lexicon = dictionarylib.doublearraylexicon.DoubleArrayLexicon(bytes_, 0)
        tokenizer = japanesetokenizer.JapaneseTokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, [])
        user_lexicon.calclate_cost(tokenizer)
        self.lexicon.append(user_lexicon)

    def read_caracter_definition(self, filename):
        if self.grammar is None:
            return
        char_category = dictionarylib.charactercategory.CharacterCategory()
        char_category.read_caracter_definition(filename)
        self.grammar.set_character_category(char_category)

    def close(self):
        self.grammar = None
        self.lexicon = None
        for buffer_ in self.buffers:
            buffer_.close()

    def create(self):
        return japanesetokenizer.JapaneseTokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, self.path_rewrite_plugins)
