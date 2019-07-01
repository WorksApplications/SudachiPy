from . import config
from . import dictionarylib
from .dictionarylib.binarydictionary import BinaryDictionary
from .dictionarylib.lexiconset import LexiconSet
from .plugin.input_text import DefaultInputTextPlugin
from .plugin.oov import get_oov_plugins
from .plugin.path_rewrite import get_path_rewrite_plugins
from .tokenizer import Tokenizer


class Dictionary:

    def __init__(self, config_path=None, resource_dir=None):
        config.settings.set_up(config_path, resource_dir)
        self.grammar = None
        self.lexicon = None
        self.input_text_plugins = []
        self.edit_connection_plugin = []
        self.oov_provider_plugins = []
        self.path_rewrite_plugins = []
        self.dictionaries = []
        self.header = None
        self._read_system_dictionary(config.settings.system_dict_path())

        # self.edit_connection_plugin = [InhibitConnectionPlugin()]
        # for p in self.edit_connection_plugin:
        #     p.set_up(self.grammar)
        #     p.edit(self.grammar)

        self._read_character_definition(config.settings.char_def_path())

        default_input_text_plugin = DefaultInputTextPlugin()
        self.input_text_plugins = [default_input_text_plugin]
        for p in self.input_text_plugins:
            p.set_up()

        self.oov_provider_plugins = get_oov_plugins()
        if not self.oov_provider_plugins:
            raise AttributeError("no OOV provider")
        for p in self.oov_provider_plugins:
            p.set_up(self.grammar)

        self.path_rewrite_plugins = get_path_rewrite_plugins()
        for p in self.path_rewrite_plugins:
            p.set_up(self.grammar)

        for filename in config.settings.user_dict_paths():
            self._read_user_dictionary(filename)

    def _read_system_dictionary(self, filename):
        if filename is None:
            raise AttributeError("system dictionary is not specified")
        dict_ = BinaryDictionary.from_system_dictionary(filename)
        self.dictionaries.append(dict_)
        self.grammar = dict_.grammar
        self.lexicon = LexiconSet(dict_.lexicon)

    def _read_user_dictionary(self, filename):
        if self.lexicon.is_full():
            raise ValueError('too many dictionaries')
        dict_ = BinaryDictionary.from_user_dictionary(filename)
        self.dictionaries.append(dict_)
        user_lexicon = dict_.lexicon
        tokenizer_ = Tokenizer(self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, [])
        user_lexicon.calculate_cost(tokenizer_)
        self.lexicon.add(user_lexicon, self.grammar.get_part_of_speech_size())
        if dict_.grammar:
            self.grammar.add_pos_list(dict_.grammar)

    def _read_character_definition(self, filename):
        if self.grammar is None:
            return
        char_category = dictionarylib.charactercategory.CharacterCategory()
        char_category.read_character_definition(filename)
        self.grammar.set_character_category(char_category)

    def close(self):
        self.grammar = None
        self.lexicon = None
        for dict_ in self.dictionaries:
            dict_.close()

    def create(self):
        return Tokenizer(
            self.grammar, self.lexicon, self.input_text_plugins, self.oov_provider_plugins, self.path_rewrite_plugins)
