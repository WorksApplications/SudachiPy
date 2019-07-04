from enum import Enum
from typing import List

from .dictionarylib.categorytype import CategoryType
from .dictionarylib.grammar import Grammar
from .dictionarylib.lexicon import Lexicon
from .lattice import Lattice
from .latticenode import LatticeNode
from .morphemelist import MorphemeList
from .plugin.input_text import InputTextPlugin
from .plugin.path_rewrite import PathRewritePlugin
from .utf8inputtext import UTF8InputText
from .utf8inputtextbuilder import UTF8InputTextBuilder


class Tokenizer:
    SplitMode = Enum("SplitMode", "A B C")

    def __init__(self, grammar: Grammar, lexicon: Lexicon, input_text_plugins: List[InputTextPlugin],
                 oov_provider_plugins: List, path_rewrite_plugins: List[PathRewritePlugin]):
        self.grammar = grammar
        self.lexicon = lexicon
        self.input_text_plugins = input_text_plugins
        self.oov_provider_plugins = oov_provider_plugins
        self.path_rewrite_plugins = path_rewrite_plugins
        self.dump_output = None
        self.lattice = Lattice(grammar)

        if self.oov_provider_plugins:
            self.default_oov_provider = self.oov_provider_plugins[-1]

    def build_lattice(self, input_: UTF8InputText):
        bytes_ = input_.get_byte_text()
        self.lattice.resize(len(bytes_))
        for i in range(len(bytes_)):
            if not input_.is_char_alignment(i) or not self.lattice.has_previous_node(i):
                continue
            iterator = self.lexicon.lookup(bytes_, i)
            has_words = False
            for word_id, end in iterator:
                has_words = True
                n = LatticeNode(self.lexicon,
                                self.lexicon.get_left_id(word_id),
                                self.lexicon.get_right_id(word_id),
                                self.lexicon.get_cost(word_id),
                                word_id)
                self.lattice.insert(i, end, n)

            # OOV
            if CategoryType.NOOOVBOW not in input_.get_char_category_types(i):
                for oov_plugin in self.oov_provider_plugins:
                    for node in oov_plugin.get_oov(input_, i, has_words):
                        has_words = True
                        self.lattice.insert(node.get_begin(), node.get_end(), node)
            if not has_words and self.default_oov_provider:
                for node in self.default_oov_provider.get_oov(input_, i, has_words):
                    has_words = True
                    self.lattice.insert(node.get_begin(), node.get_end(), node)

            if not has_words:
                raise AttributeError("there is no morpheme at " + str(i))
        self.lattice.connect_eos_node()

    def split_path(self, path: List[LatticeNode], mode: SplitMode) -> List[LatticeNode]:
        new_path = []
        for node in path:
            if mode is self.SplitMode.A:
                wids = node.get_word_info().a_unit_split
            else:  # self.SplitMode.B
                wids = node.get_word_info().b_unit_split
            if 0 <= len(wids) <= 1:
                new_path.append(node)
            else:
                offset = node.get_begin()
                for wid in wids:
                    n = LatticeNode(self.lexicon, 0, 0, 0, wid)
                    n.begin = offset
                    offset += n.get_word_info().head_word_length
                    n.end = offset
                    new_path.append(n)
        return new_path

    def tokenize(self, text: str, mode=None) -> MorphemeList:
        if not text:
            return []
        mode = mode or self.SplitMode.C

        builder = UTF8InputTextBuilder(text, self.grammar)
        for plugin in self.input_text_plugins:
            plugin.rewrite(builder)
        input_ = builder.build()
        # dump
        self.build_lattice(input_)

        if self.dump_output:
            print("=== Lattice dump:", file=self.dump_output)
            self.lattice.dump(self.dump_output)
        path = self.lattice.get_best_path()
        # dump
        path.pop()  # remove EOS
        # dump_output
        for plugin in self.path_rewrite_plugins:
            plugin.rewrite(input_, path, self.lattice)
        self.lattice.clear()
        if mode is not self.SplitMode.C:
            path = self.split_path(path, mode)
        # dump_output
        ml = MorphemeList(input_, self.grammar, self.lexicon, path)
        return ml

    def set_dump_output(self, output):
        self.dump_output = output
