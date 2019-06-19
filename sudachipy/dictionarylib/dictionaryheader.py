import struct

from sudachipy.dictionarylib.dictionarybytebuffer import DictionaryByteBuffer


class DictionaryHeader:
    __description_size = 256
    storage_size = 8 + 8 + __description_size

    def __init__(self, bytes_, offset):
        self.bytes_ = bytes_
        self.version, self.create_time = struct.unpack_from("<2Q", bytes_, offset)
        offset += 16

        len_ = 0
        while len_ < self.__description_size:
            if bytes_[offset + len_] == 0:
                break
            len_ += 1
        self.description = bytes_[offset:offset + len_].decode("utf-8")

    @staticmethod
    def __make_bytes(version, create_time, description):
        buf = DictionaryByteBuffer()
        buf = DictionaryByteBuffer(b'\x00' * (16 + 256))
        buf.seek(0)
        buf.write_int(version, 'long')
        buf.write_int(create_time, 'long')
        bdesc = description.encode('utf-8')
        if len(bdesc) > 256:
            raise ValueError('description is too long')
        buf.write(bdesc)
        return buf.getvalue()

    @classmethod
    def from_items(cls, version, create_time, description):
        return cls(cls.__make_bytes(version, create_time, description), offset=0)
