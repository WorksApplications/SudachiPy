import mmap
import os
import unittest

from sudachipy.dictionarylib.dictionaryheader import DictionaryHeader
from sudachipy.dictionarylib.dictionaryversion import DictionaryVersion


class TestDictionaryHeader(unittest.TestCase):

    def setUp(self):
        # Copied from sudachipy.dictionay.Dictionary.read_system_dictionary
        test_resources_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'resources')
        filename = os.path.join(test_resources_dir, 'system.dic')
        with open(filename, 'r+b') as system_dic:
            bytes_ = mmap.mmap(system_dic.fileno(), 0, access=mmap.ACCESS_READ)
        offset = 0
        self.header = DictionaryHeader.from_bytes(bytes_, offset)

    def test_version(self):
        self.assertEqual(DictionaryVersion.SYSTEM_DICT_VERSION, self.header.version)

    def test_create_time(self):
        self.assertTrue(self.header.create_time > 0)

    def test_description(self):
        self.assertEqual("the system dictionary for the unit tests", self.header.description)


if __name__ == '__main__':
    unittest.main()
