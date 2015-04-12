"""
Tests commands from commands subpackage.
"""

import sys

from . import unittest, capture

from architect.commands import commands
from architect.exceptions import (
    ImportProblemError,
    CommandError,
    CommandNotProvidedError,
    CommandArgumentError
)


class BaseCommandTestCase(object):
    def setUp(self):
        sys.argv = ['architect']

    def tearDown(self):
        sys.argv = []


class CommonCommandTestCase(BaseCommandTestCase, unittest.TestCase):
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


class PartitionCommandTestCase(BaseCommandTestCase, unittest.TestCase):
    def setUp(self):
        BaseCommandTestCase.setUp(self)
        sys.argv.extend(['partition'])

    def test_required_arguments_error(self):
        with capture() as (_, err):
            self.assertIn('-m/--module', err)

    def test_module_import_error(self):
        sys.argv.extend(['-m', 'foobar'])
        with capture() as (_, err):
            self.assertIn(str(ImportProblemError('no module named')), err)

    def test_no_models_in_module_error(self):
        sys.argv.extend(['-m', 'contextlib'])
        with capture() as (out, _):
            self.assertIn('unable to find any partitionable models in a module', out)
