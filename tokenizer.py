from enum import Enum, auto


class Tokenizer(object):
    class SplitMode(Enum):
        A = auto()
        B = auto()
        C = auto()

    def tokenize(self, text, mode=SplitMode.C):
        pass

    def set_dump_output(self, output):
        pass
