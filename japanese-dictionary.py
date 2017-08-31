import mmap

from . import Settings
from dictionary import CharacterCategory
from dictionary import DoubleArrayLexicon
from dictionary import Grammar
from dictionary import GrammarImpl
from dictionary import LexiconSet


class JapaneseDictionary():
    def __init__(self, json_string, path=None):
        self.grammar = None
        self.lexicon = None
        self.input_text_plugins = []
        self.oov_provider_plugins = []
        self.path_rewrite_plugins = []
        self.buffers = []

        if path is None:
            pass

        self.settings = Settings.parse_settings(path, json_string)

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
        try:
            bytes_ = mmap.mmap()
