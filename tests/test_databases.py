"""
Tests database specific behaviour which is independent from ORM being used.
"""

import os

from . import unittest, mock

from architect.databases.postgresql.partition import Partition, RangePartition
from architect.exceptions import (
    PartitionConstraintError,
    PartitionRangeSubtypeError
)


class BasePartitionTestCase(object):
    def setUp(self):
        model = mock.Mock(__name__='Foo')
        defaults = {'table': None, 'column_value': None, 'column': None, 'pk': None}
        self.partition = Partition(model, **defaults)
        self.range_partition = RangePartition(model, **dict(constraint='foo', subtype='bar', **defaults))


@unittest.skipUnless(os.environ.get('DB') == 'sqlite', 'Not a SQLite build')
class SQLitePartitionTestCase(BasePartitionTestCase, unittest.TestCase):
    pass


@unittest.skipUnless(os.environ.get('DB') == 'postgresql', 'Not a PostgreSQL build')
class PostgresqlPartitionTestCase(BasePartitionTestCase, unittest.TestCase):
    def test__get_definitions_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.partition._get_definitions())

    def test__get_definitions_raises_partition_range_subtype_error(self):
        self.assertRaises(PartitionRangeSubtypeError, lambda: self.range_partition._get_definitions())

    def test__get_date_definitions_raises_partition_constraint_error(self):
        self.range_partition.subtype = 'date'
        self.assertRaises(PartitionConstraintError, lambda: self.range_partition._get_definitions())

    def test__get_integer_definitions_raises_partition_constraint_error(self):
        self.range_partition.subtype = 'integer'
        self.assertRaises(PartitionConstraintError, lambda: self.range_partition._get_definitions())

    def test__get_string_firstchars_definitions_raises_partition_constraint_error(self):
        self.range_partition.subtype = 'string_firstchars'
        self.assertRaises(PartitionConstraintError, lambda: self.range_partition._get_definitions())

    def test__get_string_lastchars_definitions_raises_partition_constraint_error(self):
        self.range_partition.subtype = 'string_lastchars'
        self.assertRaises(PartitionConstraintError, lambda: self.range_partition._get_definitions())


@unittest.skipUnless(os.environ.get('DB') == 'mysql', 'Not a MySQL build')
class MysqlPartitionTestCase(BasePartitionTestCase, unittest.TestCase):
    pass
