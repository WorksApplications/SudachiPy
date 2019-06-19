from io import BytesIO


class DictionaryByteBuffer(BytesIO):

    def write_int(self, int_, type_):
        if type_ == 'byte':
            len_ = 1
        elif type_ == 'int':
            len_ = 4
        elif type_ == 'char':
            len_ = 2
        elif type_ == 'short':
            len_ = 2
        else:
            raise ValueError('{} is invalid type'.format(type_))
        self.write(int_.to_bytes(len_, byteorder='little'))

    def write_str(self, text):
        self.write(text.encode('utf-16-le'))
