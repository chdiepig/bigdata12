from unittest import TestCase
from utils.file_util import get_dir_files_list


class TestFileUtil(TestCase):
    def test_get_file_util_list(self):
        result = get_dir_files_list('../data')
        self.assertEqual(result,
                         ['../data/x00', '../data/x01', '../data/x02', '../data/x03',
                          '../data/x04', '../data/x05', '../data/x06'])
