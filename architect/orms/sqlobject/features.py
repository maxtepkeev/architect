"""
Defines features for the SQLObject ORM.
"""

from sqlobject.main import instanceName

from ..bases import BasePartitionFeature, BaseOperationFeature


class OperationFeature(BaseOperationFeature):
    def __init__(self, *args, **kwargs):
        super(OperationFeature, self).__init__(*args, **kwargs)
        self.connection = self.model_cls._connection

    def execute(self, sql, autocommit=True):
        self.connection.autoCommit = autocommit
        return self.connection.query(sql)

    def select_one(self, sql):
        result = self.connection.queryOne(sql)
        return result[0] if result is not None else result

    def select_all(self, sql, as_dict=False):
        if as_dict:
            result = [dict(zip([c[0] for c in desc], row)) for desc, row in self.connection.queryAllDescription(sql)]
        else:
            result = self.connection.queryAll(sql)

        return result


class PartitionFeature(BasePartitionFeature):
    decorate = ('_create',)

    @property
    def model_meta(self):
        return {
            'table': self.model_cls.sqlmeta.table,
            'pk': self.model_cls.sqlmeta.idName,
            'dialect': self.model_cls._connection.dbName,
            'column_value': self._column_value(self.model_cls.sqlmeta.columns.keys()),
        }

    @staticmethod
    def _decorate__create(method):
        """
        Checks if partition exists and creates it if needed before saving model instance.
        """
        def wrapper(instance, *args, **kwargs):
            for col, val in instance.sqlmeta.columns.items():
                setattr(instance, instanceName(col), kwargs.get(col, val.default))

            partition = instance.architect.partition.get_partition()

            if not partition.exists():
                partition.create()

            for col in instance.sqlmeta.columns:
                delattr(instance, instanceName(col))

            method(instance, *args, **kwargs)
        return wrapper
