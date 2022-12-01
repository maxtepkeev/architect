"""
Tests database specific behaviour which is independent from ORM being used.
"""
from . import unittest, mock
from architect.orms.decorators import set_list_vals


class SetListValsTestCase(unittest.TestCase):
    def test__get_command_str_single_column(self):
        options = {
            'column': 'dfs'
        }
        assert set_list_vals('column', **options)['columns'][0] == 'dfs'
