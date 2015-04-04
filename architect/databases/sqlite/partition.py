"""
SQLite doesn't support table partitioning, but is often used as a primary
database during tests, that is the main reason why this dummy partitioning
implementation exists.
"""

from ..bases import BasePartition


class Partition(BasePartition):
    def prepare(self):
        pass

    def exists(self):
        return False

    def create(self):
        pass


class RangePartition(Partition):
    pass
