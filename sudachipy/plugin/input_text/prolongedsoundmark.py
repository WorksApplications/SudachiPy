from . import InputTextPlugin


class ProlongedSoundMarkInputTextPlugin(InputTextPlugin):

    def __init__(self, json_obj):
        self._psm_set = set()
        self._replace_symbol = 'ー'
        if not json_obj:
            return
        if 'prolongedSoundMarks' in json_obj:
            self._psm_set = set([ord(psm) for psm in json_obj['prolongedSoundMarks']])
        if 'replacementSymbol' in json_obj:
            self._replace_symbol = json_obj['replacementSymbol']

    def set_up(self) -> None:
        pass

    def rewrite(self, builder: InputTextPlugin.Builder) -> None:
        text = builder.get_text()
        n = len(text)
        offset = 0
        is_psm = False
        m_start_idx = n
        for i in range(n):
            cp = ord(text[i])
            if not is_psm and cp in self._psm_set:
                is_psm = True
                m_start_idx = i
            elif is_psm and cp not in self._psm_set:
                if i - m_start_idx > 1:
                    builder.replace(m_start_idx - offset, i - offset, self._replace_symbol)
                    offset += i - m_start_idx - 1
                is_psm = False
        if is_psm and n - m_start_idx > 1:
            builder.replace(m_start_idx - offset, n - offset, self._replace_symbol)
