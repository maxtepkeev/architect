from tests import unittest

from architect.databases import BasePartition
from architect.orms import BasePartitionableMixin


class BasePartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Partition = type('Partition', (BasePartition,), {})(
            column_value=None,
            partition_column=None,
            execute=None,
            model=None,
            table=None,
            pk=None
        )

    def test_prepare_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.prepare())

    def test_exists_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.exists())

    def test_create_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition.create())

    def test_get_name_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition._get_name())

    def test_get_partition_function_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.Partition._get_partition_function())


class BasePartitionableMixinTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.PartitionableMixinCls = type('PartitionableMixin', (BasePartitionableMixin,), {})
        cls.PartitionableMixin = cls.PartitionableMixinCls()

    def test_raises_database_error(self):
        from architect.exceptions import DatabaseError
        self.PartitionableMixinCls.model_meta = property(lambda self: {'database': 'foo'})
        self.assertRaises(DatabaseError, lambda: self.PartitionableMixinCls().get_database())

    def test_raises_partition_type_error(self):
        from architect.exceptions import PartitionTypeError
        self.PartitionableMixinCls.model_meta = property(lambda self: {'database': 'sqlite'})
        self.assertRaises(PartitionTypeError, lambda: self.PartitionableMixin.get_partition())

    def test_partitionable_meta_defaults(self):
        self.assertEqual(self.PartitionableMixin.PartitionableMeta.partition_type, 'None')
        self.assertEqual(self.PartitionableMixin.PartitionableMeta.partition_subtype, 'None')
        self.assertEqual(self.PartitionableMixin.PartitionableMeta.partition_range, 'None')
        self.assertEqual(self.PartitionableMixin.PartitionableMeta.partition_column, 'None')

    def test_model_meta_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.PartitionableMixin.model_meta)

    def test_execute_raw_sql_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.PartitionableMixin.execute_raw_sql(None))

    def test_get_empty_instance_not_implemented(self):
        self.assertRaises(NotImplementedError, lambda: self.PartitionableMixin.get_empty_instance())
