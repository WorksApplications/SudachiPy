def constant(f):

    def fset(self, value):
        raise TypeError

    def fget(self):
        return f()

    return property(fget, fset)


class _DictionaryVersion:

    @constant
    def SYSTEM_DICT_VERSION():
        return 0x7366d3f18bd111e7

    @constant
    def USER_DICT_VERSION():
        return 0xa50f31188bd211e7


DictionaryVersion = _DictionaryVersion()
