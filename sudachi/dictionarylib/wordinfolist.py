class WordInfoList(object):
    def __init__(self, bytes_, offset, word_size):
        self.bytes = bytes_
        self.offset = offset

    def get_word_info(self, word_id):
        index = self.word_id_to_offset(word_id)

        surface = self.buffer_to_string(index)
        index += 1 + 2 * len(surface)
        self.bytes.seek(index)
        headword_length = self.bytes.read_byte()
        index += 1
        pos_id = int.from_bytes(self.bytes.read(2), 'little')
        
