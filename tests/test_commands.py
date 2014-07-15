from tests import sys, unittest, capture

from architect.commands import commands
from architect.exceptions import (
    ImportProblemError,
    CommandError,
    CommandNotProvidedError,
    CommandArgumentError
)


class CommandLineTestCase(unittest.TestCase):
    def setUp(self):
        sys.argv = ['architect']

    def test_no_command_provided_error(self):
        with capture() as (_, err):
            self.assertIn(str(CommandNotProvidedError(allowed=commands.keys())).lower(), err)

    def test_invalid_command_error(self):
        sys.argv.append('foobar')
        with capture() as (_, err):
            self.assertIn(str(CommandError(current='foobar', allowed=commands.keys())).lower(), err)

    def test_command_invalid_argument(self):
        sys.argv.extend(['partition', '-m', 'foobar', '-foo', 'bar'])
        with capture() as (_, err):
            self.assertIn(str(CommandArgumentError(current='-foo bar', allowed='')).lower(), err)

    def test_partition_command_required_arguments_error(self):
        sys.argv.extend(['partition'])
        with capture() as (_, err):
            self.assertIn('-m/--module', err)

    def test_partition_command_module_import_error(self):
        sys.argv.extend(['partition', '-m', 'foobar'])
        with capture() as (_, err):
            self.assertIn(str(ImportProblemError('no module named')), err)

    def test_partition_command_no_models_error(self):
        sys.argv.extend(['partition', '-m', 'contextlib'])
        with capture() as (out, _):
            self.assertIn('unable to find any partitionable models in a module', out)

    def tearDown(self):
        sys.argv = []
