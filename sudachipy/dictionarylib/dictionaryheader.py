import struct


class DictionaryHeader:
    __description_size = 256
    storage_size = 8 + 8 + __description_size

    def __init__(self, bytes_, offset):
        self.version, self.create_time = struct.unpack_from("<2Q", bytes_, offset)
        offset += 16

        len_ = 0
        while len_ < self.__description_size:
            if bytes_[offset + len_] == 0:
                break
            len_ += 1
        self.description = bytes_[offset:offset + len_].decode("utf-8")
