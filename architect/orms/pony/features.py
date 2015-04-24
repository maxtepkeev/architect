"""
Defines features for the Pony ORM.
"""

from pony.orm.core import db_session

from ..bases import BasePartitionFeature, BaseOperationFeature


class OperationFeature(BaseOperationFeature):
    def execute(self, sql, autocommit=True):
        with db_session:
            return self.model_cls._database_._exec_sql(sql)


class PartitionFeature(BasePartitionFeature):
    decorate = ('_save_',)

    @property
    def model_meta(self):
        return {
            'table': self.model_cls._table_,
            'pk': self.model_cls._pk_columns_,
            'dialect': self.model_cls._database_.provider.dialect.lower(),
            'column_value': self._column_value(self.model_cls._columns_),
        }

    @staticmethod
    def _decorate__save_(method):
        """
        Checks if partition exists and creates it if needed before saving model instance.
        """
        @db_session
        def wrapper(instance, *args, **kwargs):
            partition = instance.architect.partition.get_partition()

            if not partition.exists():
                partition.create()

            method(instance, *args, **kwargs)
        return wrapper
