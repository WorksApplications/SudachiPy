import json
import unittest

from sudachipy.dictionarylib.dictionaryversion import DictionaryVersion
from sudachipy import config, dictionary


class TestDictionaryHeader(unittest.TestCase):

    def setUp(self):
        with open(config.SETTINGFILE, "r", encoding="utf-8") as f:
            settings = json.load(f)
        self.dict_ = None
        self.tokenizer_obj = None
        try:
            self.dict_ = dictionary.Dictionary(settings)
            self.tokenizer_obj = self.dict_.create()
        except FileNotFoundError:
            self.fail('dictionary isn\'t prepared properly')

    def test_version(self):
        self.assertEqual(DictionaryVersion.SYSTEM_DICT_VERSION, self.dict_.header.version)

    def test_createtime(self):
        self.assertTrue(self.dict_.header.create_time > 0)

    # def test_description(self):
    #     self.assertEqual("the system dictionary for the unit tests", self.dict_.header.description)


if __name__ == '__main__':
    unittest.main()
