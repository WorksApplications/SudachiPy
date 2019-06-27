from abc import ABC, abstractmethod

from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder


class InputTextPlugin(ABC):

    Builder = UTF8InputTextBuilder

    @abstractmethod
    def set_up(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rewrite(self, builder: Builder) -> None:
        raise NotImplementedError
