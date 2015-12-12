"""
Defines features for the Peewee ORM.
"""

from peewee import CompositeKey

from ..bases import BasePartitionFeature, BaseOperationFeature


class OperationFeature(BaseOperationFeature):
    def execute(self, sql, autocommit=True):
        return self.model_cls._meta.database.execute_sql(sql.replace('%', '%%'), require_commit=autocommit)


class PartitionFeature(BasePartitionFeature):
    decorate = ('save',)

    @property
    def model_meta(self):
        meta = self.model_cls._meta
        pk = meta.primary_key

        return {
            'table': meta.db_table,
            'pk': list(pk.field_names) if isinstance(pk, CompositeKey) else pk.name,
            'dialect': meta.database.__class__.__name__.lower().replace('database', ''),
            'column_value': self._column_value([field for field in meta.fields.keys()]),
        }

    @staticmethod
    def _decorate_save(method):
        """
        Checks if partition exists and creates it if needed before saving model instance.
        """
        def wrapper(instance, *args, **kwargs):
            partition = instance.architect.partition.get_partition()

            if not partition.exists():
                partition.create()

            method(instance, *args, **kwargs)
        return wrapper
