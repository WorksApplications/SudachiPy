from io import BytesIO


class DictionaryByteBuffer(BytesIO):

    def write_int(self, int_, type_):
        if type_ == 'byte':
            len_ = 1
        elif type_ == 'int':
            len_ = 4
        elif type_ == 'char' or type_ == 'short':
            len_ = 2
        elif type_ == 'long':
            len_ = 8
        else:
            raise ValueError('{} is invalid type'.format(type_))
        if int_ == -1:
            int_ = 0x0ff
        self.write(int_.to_bytes(len_, byteorder='little', signed=False))

    def write_str(self, text):
        self.write(text.encode('utf-16-le'))
