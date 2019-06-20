from io import BytesIO


class DictionaryByteBuffer(BytesIO):

    __ENDIAN = 'little'

    def write_int(self, int_, type_, signed=True):
        if type_ == 'byte':
            len_ = 1
            signed = False
        elif type_ == 'int':
            len_ = 4
        elif type_ == 'char':
            len_ = 2
            signed = False
        elif type_ == 'short':
            len_ = 2
        elif type_ == 'long':
            len_ = 8
        else:
            raise ValueError('{} is invalid type'.format(type_))
        # print(int_, type_, len_)
        self.write(int_.to_bytes(len_, byteorder=self.__ENDIAN, signed=signed))

    def write_str(self, text):
        self.write(text.encode('utf-16-le'))

    def clear(self):
        self.seek(0)
        self.truncate(0)
