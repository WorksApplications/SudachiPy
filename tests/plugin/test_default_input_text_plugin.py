import unittest

from sudachipy.plugin.input_text.default_input_text_plugin import DefaultInputTextPlugin
from sudachipy.utf8inputtextbuilder import UTF8InputTextBuilder
from tests import mock_grammar


class TestDefaultInputTextPlugin(unittest.TestCase):

    original_text = "ÂＢΓД㈱ｶﾞウ゛⼼Ⅲ"
    normalized_text = "âbγд(株)ガヴ⼼ⅲ"

    def setUp(self):
        self.builder = UTF8InputTextBuilder(self.original_text, mock_grammar.mocked_grammar)
        self.plugin = DefaultInputTextPlugin()
        try:
            self.plugin.set_up()
        except IOError:
            self.fail('no file')

    def test_before_rewrite(self):
        self.assertEqual(self.original_text, self.builder.get_original_text())
        self.assertEqual(self.original_text, self.builder.get_text())
        text = self.builder.build()
        self.assertEqual(self.original_text, text.get_original_text())
        self.assertEqual(self.original_text, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(30, len(bytes_))
        expected = b'\xc3\x82\xef\xbc\xa2\xce\x93\xd0\x94\xe3\x88\xb1\xef\xbd\xb6\xef\xbe\x9e\xe3\x82\xa6\xe3\x82\x9b\xe2\xbc\xbc\xe2\x85\xa2'
        self.assertEqual(expected, bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(0, text.get_original_index(1))
        self.assertEqual(1, text.get_original_index(2))
        self.assertEqual(1, text.get_original_index(4))
        self.assertEqual(3, text.get_original_index(8))
        self.assertEqual(5, text.get_original_index(12))
        self.assertEqual(9, text.get_original_index(24))
        self.assertEqual(9, text.get_original_index(26))

    def test_after_write(self):
        self.assertEqual(self.original_text, self.builder.get_original_text())
        self.assertEqual(self.original_text, self.builder.get_text())
        self.plugin.rewrite(self.builder)
        text = self.builder.build()
        self.assertEqual(self.original_text, text.get_original_text())
        self.assertEqual(self.normalized_text, text.get_text())
        bytes_ = text.get_byte_text()
        self.assertEqual(24, len(bytes_))
        expected = b'\xc3\xa2\x62\xce\xb3\xd0\xb4\x28\xe6\xa0\xaa\x29\xe3\x82\xac\xe3\x83\xb4\xe2\xbc\xbc\xe2\x85\xb2'
        self.assertEqual(expected, bytes_)
        self.assertEqual(0, text.get_original_index(0))
        self.assertEqual(0, text.get_original_index(1))
        self.assertEqual(1, text.get_original_index(2))
        self.assertEqual(2, text.get_original_index(3))
        self.assertEqual(4, text.get_original_index(7))
        self.assertEqual(4, text.get_original_index(11))
        self.assertEqual(7, text.get_original_index(15))
        self.assertEqual(7, text.get_original_index(17))

    # def test_setup_with_null(self):

    def test_invalid_format_ignorelist(self):
        plugin = DefaultInputTextPlugin()
        try:
            plugin.read_rewrite_lists('tests/resources/rewrite_error_ignorelist.def')
            self.fail('no error occurred')
        except RuntimeError:
            pass

    def test_invalid_format_replacelist(self):
        plugin = DefaultInputTextPlugin()
        try:
            plugin.read_rewrite_lists('tests/resources/rewrite_error_replacelist.def')
            self.fail('no error occurred')
        except RuntimeError:
            pass

    def test_duplicated_lines_replacelist(self):
        plugin = DefaultInputTextPlugin()
        try:
            plugin.read_rewrite_lists('tests/resources/rewrite_error_dup.def')
            self.fail('no error occurred')
        except RuntimeError:
            pass


if __name__ == '__main__':
    unittest.main()
