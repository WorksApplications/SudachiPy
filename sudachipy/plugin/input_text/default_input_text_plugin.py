import os

from sudachipy import config


class DefaultInputTextPlugin:
    def __init__(self):
        self.ignore_normalize_set = set()
        self.key_lengths = {}
        self.replace_char_map = {}

    def set_up(self):
        rewrite_def = os.path.join(config.RESOURCEDIR, "rewrite.def")
        if not rewrite_def:
            raise AttributeError("rewriteDef is not defined")
        self.read_rewrite_lists(rewrite_def)

    def rewrite(self, builder):
        offset = 0
        next_offset = 0
        text = builder.get_text()

        # 1. replace char without normalize
        # 2. normalize
        # 2-1. capital alphabet (not only Latin but Greek, Cyrillic, etc.) -> small
        # 2-2. normalize (except in ignoreNormalize)
        #   e.g. full-width alphabet -> half-width / ligature / etc.

    def read_rewrite_lists(self, rewrite_def):
        with open(rewrite_def, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                cols = line.split()

                # ignored normalize list
                if len(cols) == 1:
                    key = cols[0]
                    self.ignore_normalize_set.add(key)
                # replace char list
                elif len(cols) == 2:
                    if cols[0] in self.replace_char_map:
                        raise RuntimeError("{} is already defined at line {}".format(cols[0], i))
                    self.key_lengths[cols[0]] = len(cols[0])
                    self.replace_char_map[cols[0]] = cols[1]
                else:
                    raise RuntimeError("invalid format at line {}".format(i))
