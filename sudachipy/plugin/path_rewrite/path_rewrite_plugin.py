from abc import ABC, abstractmethod

from sudachipy.dictionarylib.wordinfo import WordInfo


class PathRewritePlugin(ABC):

    @abstractmethod
    def set_up(self, grammar):
        raise NotImplementedError

    @abstractmethod
    def rewrite(self, text, path, lattice):
        raise NotImplementedError

    def concatenate(self, path, begin, end, lattice, normalized_form):
        if begin >= end:
            raise IndexError("begin >= end")
        b = path[begin].get_begin()
        e = path[end - 1].get_end()
        pos_id = path[begin].get_word_info().pos_id
        surface = ""
        length = 0
        normalized_builder, dictionary_builder, reading_builder = "", "", ""
        for i in range(begin, end):
            info = path[i].get_word_info()
            surface += info.surface
            length += info.head_word_length
            if not normalized_form:
                normalized_builder += info.normalized_form
            dictionary_builder += info.dictionary_form
            reading_builder += info.reading_form

        normalized_form = normalized_form if normalized_form else normalized_builder
        wi = WordInfo(surface=surface, head_word_length=length, pos_id=pos_id,
                      normalized_form=normalized_form, dictionary_form=dictionary_builder, dictionary_form_word_id=-1,
                      reading_form=reading_builder, a_unit_split=[], b_unit_split=[], word_structure=[])

        node = lattice.create_node()
        node.set_range(b, e)
        node.set_word_info(wi)

        path[begin:end] = [node]
        return node

    def concatenate_oov(self, path, begin, end, pos_id, lattice):
        if begin >= end:
            raise IndexError("begin >= end")
        b = path[begin].get_begin()
        e = path[end - 1].get_end()
        surface = ""
        length = 0
        for i in range(begin, end):
            info = path[i].get_word_info()
            surface += info.surface
            length += info.head_word_length

        wi = WordInfo(surface=surface, head_word_length=length, pos_id=pos_id,
                      normalized_form=surface, dictionary_form=surface, dictionary_form_word_id=-1,
                      reading_form="", a_unit_split=[], b_unit_split=[], word_structure=[])

        node = lattice.create_node()
        node.set_range(b, e)
        node.set_word_info(wi)

        path[begin:end] = [node]
        return node

    def get_char_category_types(self, text, node):
        return text.get_char_category_types(node.get_begin(), node.get_end())
