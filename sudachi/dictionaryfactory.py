from . import japanesedictionary


class DictionaryFactory(object):
    def create(self, settings, path=None):
        if path is None:
            return japanesedictionary.JapaneseDictionary(settings)
        else:
            return japanesedictionary.JapaneseDictionary(settings, path)
