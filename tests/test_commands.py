import sys
from contextlib import contextmanager

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from tests import unittest
from architect.commands import main, commands
from architect.exceptions import (
    ImportProblemError,
    CommandError,
    CommandNotProvidedError,
    CommandArgumentError
)


@contextmanager
def capture():
    out, sys.stderr = sys.stderr, StringIO()

    try:
        main()
    except SystemExit:
        pass

    sys.stderr.seek(0)
    yield sys.stderr.read().strip()
    sys.stderr = out


class CommandLineTestCase(unittest.TestCase):
    def setUp(self):
        sys.argv = ['architect']

    def test_no_command_provided_error(self):
        with capture() as output:
            self.assertIn(str(CommandNotProvidedError(allowed=commands.keys())).lower(), output)

    def test_invalid_command_error(self):
        sys.argv.append('foobar')
        with capture() as output:
            self.assertIn(str(CommandError(current='foobar', allowed=commands.keys())).lower(), output)

    def test_command_invalid_argument(self):
        sys.argv.extend(['partition', '-m', 'foobar', '-foo', 'bar'])
        with capture() as output:
            self.assertIn(str(CommandArgumentError(current='-foo bar', allowed='')).lower(), output)

    def test_partition_command_required_arguments_error(self):
        sys.argv.extend(['partition'])
        with capture() as output:
            self.assertIn('-m/--module', output)

    def test_partition_command_module_import_error(self):
        sys.argv.extend(['partition', '-m', 'foobar'])
        with capture() as output:
            self.assertIn(str(ImportProblemError('no module named')), output)

    def tearDown(self):
        sys.argv = []
