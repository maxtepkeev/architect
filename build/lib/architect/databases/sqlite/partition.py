"""
SQLite doesn't support table partitioning, but it's often used as a primary
database during tests, that is the main reason why this dummy partitioning
implementation exists.
"""

from architect.databases import BasePartition


class Partition(BasePartition):
    """Common methods for all partition types"""
    def prepare(self):
        pass

    def exists(self):
        """Checks if partition exists"""
        return True

    def create(self):
        """Creates new partition"""
        pass


class RangePartition(Partition):
    """Range partition type implementation"""
    pass
