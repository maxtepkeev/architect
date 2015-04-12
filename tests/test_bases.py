"""
Tests base classes only.
"""

from . import unittest, mock

from architect.databases.bases import BasePartition
from architect.orms.bases import BaseOperationFeature, BasePartitionFeature


class BasePartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Partition = BasePartition(mock.Mock(), table=None, column_value=None, column=None, pk=None)

    def test_prepare_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.prepare())

    def test_exists_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.exists())

    def test_create_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.create())


class BaseOperationFeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.OperationFeature = BaseOperationFeature(mock.Mock(), mock.Mock(__name__='Foo'), **{})

    def test_execute_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.OperationFeature.execute(''))


class BasePartitionFeatureTestCase(unittest.TestCase):
    def setUp(self):
        self.PartitionFeatureCls = type('PartitionFeature', (BasePartitionFeature,), {})
        self.PartitionFeature = self.PartitionFeatureCls(mock.Mock(), mock.Mock(__name__='Foo'), **{})

    def test_get_partition_raises_database_error(self):
        from architect.exceptions import DatabaseError
        self.PartitionFeatureCls.model_meta = property(lambda obj: {'dialect': 'foo'})
        self.assertRaises(DatabaseError, lambda: self.PartitionFeature.get_partition())

    def test_get_partition_raises_option_not_set_error(self):
        from architect.exceptions import OptionNotSetError
        self.PartitionFeatureCls.model_meta = property(lambda obj: {'dialect': 'sqlite'})
        self.assertRaises(OptionNotSetError, lambda: self.PartitionFeature.get_partition())

    def test_get_partition_raises_partition_type_error(self):
        from architect.exceptions import PartitionTypeError
        self.PartitionFeatureCls.model_meta = property(lambda obj: {'dialect': 'sqlite'})
        self.PartitionFeature.options = {'type': 'foo'}
        self.assertRaises(PartitionTypeError, lambda: self.PartitionFeature.get_partition())

    def test_model_meta_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.PartitionFeature.model_meta)

    def test_column_value_raises_option_not_set_error(self):
        from architect.exceptions import OptionNotSetError
        self.assertRaises(OptionNotSetError, lambda: self.PartitionFeature._column_value([]))

    def test_column_value_raises_partition_column_error(self):
        from architect.exceptions import PartitionColumnError
        self.PartitionFeature.options = {'column': 'foo'}
        self.PartitionFeature.model_obj = mock.Mock(spec=[])
        self.assertRaises(PartitionColumnError, lambda: self.PartitionFeature._column_value([]))
