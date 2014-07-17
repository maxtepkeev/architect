from architect.orms import BasePartitionableMixin


class AbstractPartitionableModel(BasePartitionableMixin):
    """Abstract partitionable model used for tests not connected to specific ORM"""

    @property
    def model_meta(self):
        return {
            'table': None,
            'pk': None,
            'database': 'postgresql',
            'column_value': None,
        }

    def execute_raw_sql(self, sql):
        return lambda: None

    @classmethod
    def get_empty_instance(cls, dsn=None):
        return cls()
