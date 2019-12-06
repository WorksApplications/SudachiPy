# Copyright (c) 2019 Works Applications Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
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
    """ tokenizer of morphological analysis

    Attributes:
        SplitMode:
            split mode to change words continuation.
            A == short mode
            B == middle mode
            C == long mode
        _dump_output:
            file object to dump lattice structure
        _grammar:

        _input_text_plugins:

        _lattice:

        _lexicon:

        _mode:

        _oov_provider_plugins:

        _path_rewrite_plugins:

    """

    SplitMode = Enum("SplitMode", "A B C")

    def __init__(self, grammar: Grammar, lexicon: Lexicon, input_text_plugins: List[InputTextPlugin],
                 oov_provider_plugins: List, path_rewrite_plugins: List[PathRewritePlugin],
                 mode: SplitMode = None):
        self._grammar = grammar
        self._lexicon = lexicon
        self._input_text_plugins = input_text_plugins
        self._oov_provider_plugins = oov_provider_plugins
        self._path_rewrite_plugins = path_rewrite_plugins
        self._dump_output = open(os.devnull, 'w')
        self._lattice = Lattice(grammar)
        self._mode = mode or self.SplitMode.C
        self._logger = logging.getLogger(__name__)
        self._logger.disabled = True
        if self._oov_provider_plugins:
            self.default_oov_provider = self._oov_provider_plugins[-1]

    def tokenize(self, text: str, mode=None, logger=None) -> MorphemeList:
        """ tokenize a text.

        In default tokenize text with SplitMode.C

        Args:
            text: input text
            mode: split mode
            logger: if True output lattice structure
        Returns:
            list of morpheme (MorphemeList)

        """
        if not text:
            return MorphemeList.empty()

        mode = mode or self._mode
        logger = logger or self._logger

        builder = UTF8InputTextBuilder(text, self._grammar)
        for plugin in self._input_text_plugins:
            plugin.rewrite(builder)
        input_ = builder.build()
        logger.info('=== Inupt dump:')
        logger.info(input_.get_text())

        self._build_lattice(input_)

        logger.info('=== Lattice dump:')
        self._lattice.dump(logger)

        path = self._lattice.get_best_path()

        logger.info('=== Before Rewriting:')
        self._dump_path(path, logger)

        for plugin in self._path_rewrite_plugins:
            plugin.rewrite(input_, path, self._lattice)
        self._lattice.clear()

        path = self._split_path(path, mode)

        logger.info('=== After Rewriting:')
        self._dump_path(path, logger)
        logger.info('===')

        ml = MorphemeList(input_, self._grammar, self._lexicon, path)
        return ml

    def _build_lattice(self, input_: UTF8InputText):
        bytes_ = input_.get_byte_text()
        self._lattice.resize(len(bytes_))
        for i in range(len(bytes_)):
            if not input_.can_bow(i) or not self._lattice.has_previous_node(i):
                continue
            iterator = self._lexicon.lookup(bytes_, i)
            has_words = False
            for word_id, end in iterator:
                if (end < len(bytes_)) and (not input_.can_bow(end)):
                    continue
                has_words = True
                n = LatticeNode(self._lexicon,
                                self._lexicon.get_left_id(word_id),
                                self._lexicon.get_right_id(word_id),
                                self._lexicon.get_cost(word_id),
                                word_id)
                self._lattice.insert(i, end, n)

            # OOV
            if CategoryType.NOOOVBOW not in input_.get_char_category_types(i):
                for oov_plugin in self._oov_provider_plugins:
                    for node in oov_plugin.get_oov(input_, i, has_words):
                        has_words = True
                        self._lattice.insert(node.get_begin(), node.get_end(), node)
            if not has_words and self.default_oov_provider:
                for node in self.default_oov_provider.get_oov(input_, i, has_words):
                    has_words = True
                    self._lattice.insert(node.get_begin(), node.get_end(), node)

            if not has_words:
                raise RuntimeError("there is no morpheme at " + str(i))
        self._lattice.connect_eos_node()

    def _split_path(self, path: List[LatticeNode], mode: SplitMode) -> List[LatticeNode]:
        if mode == self.SplitMode.C:
            return path
        new_path = []
        for node in path:
            if mode is self.SplitMode.A:
                wids = node.get_word_info().a_unit_split
            else:
                wids = node.get_word_info().b_unit_split
            if len(wids) <= 1:
                new_path.append(node)
            else:
                offset = node.get_begin()
                for wid in wids:
                    n = LatticeNode(self._lexicon, 0, 0, 0, wid)
                    n.begin = offset
                    offset += n.get_word_info().head_word_length
                    n.end = offset
                    new_path.append(n)
        return new_path

    def _dump_path(self, path: List[LatticeNode], logger) -> None:
        if logger.disabled:
            return
        for i, node in enumerate(path):
            logger.info('{}: {}￿'.format(i, node))
