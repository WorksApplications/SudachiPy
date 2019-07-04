from sudachipy import config

from . import InputTextPlugin


class ProlongedSoundMarkInputTextPlugin(InputTextPlugin):

    def __init__(self):
        self.psm_set = set()
        self.replace_symbol = ''

    def set_up(self) -> None:
        for s in config.settings['prolongedSoundMarks']:
            self.psm_set.add(ord(s[0]))
        self.replace_symbol = config.settings['replacementSymbol']

    def rewrite(self, builder: InputTextPlugin.Builder) -> None:
        text = builder.get_text()
        n = len(text)
        offset = 0
        is_psm = False
        m_start_idx = n
        for i in range(n):
            cp = ord(text[i])
            if not is_psm and cp in self.psm_set:
                is_psm = True
                m_start_idx = i
            elif is_psm and cp not in self.psm_set:
                if (i - m_start_idx) > 1:
                    builder.replace(m_start_idx - offset, i - offset, self.replace_symbol)
                    offset += i - m_start_idx - 1
                is_psm = False
        if is_psm and (n - m_start_idx) > 1:
            builder.replace(m_start_idx - offset, n - offset, self.replace_symbol)
