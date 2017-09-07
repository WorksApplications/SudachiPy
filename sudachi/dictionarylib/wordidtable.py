class WordIdTable(object):
    def __init__(self, bytes_, offset):
        self.bytes = bytes_
        bytes_.seek(offset)
        self.size = int.from_bytes(bytes_.read(4), 'little')
        self.offset = offset + 4

    def storage_size(self):
        return 4 + self.size

    def get(self, index):
        self.bytes.seek(self.offset + index)
        length = int.from_bytes(self.bytes.read_byte())
        index += 1
        result = [0 for i in range(length)]
        for i in range(length):
            self.bytes.seek(self.offset + index)
            result[i] = int.from_bytes(self.bytes.read(4), 'little')
            index += 4
        return result
