"""
Defines features for the Django ORM.
"""

from django.db import connection, transaction
from django.db.models.fields import FieldDoesNotExist

from ...orms.bases import BasePartitionFeature, BaseOperationFeature
from ...exceptions import PartitionColumnError, OptionNotSetError


class OperationFeature(BaseOperationFeature):
    def __init__(self, *args, **kwargs):
        super(OperationFeature, self).__init__(*args, **kwargs)
        self.cursor = connection.cursor()

    def execute(self, sql, autocommit=True):
        if not autocommit:
            return self.cursor.execute(sql)

        try:
            autocommit = transaction.atomic  # Django >= 1.6
        except AttributeError:
            autocommit = transaction.commit_on_success  # Django <= 1.5

        with autocommit():
            return self.cursor.execute(sql)

    def select_one(self, sql):
        self.execute(sql)
        result = self.cursor.fetchone()
        return result[0] if result is not None else result

    def select_all(self, sql, as_dict=False):
        self.execute(sql)

        if as_dict:
            result = [dict(zip([col[0] for col in self.cursor.description], row)) for row in self.cursor.fetchall()]
        else:
            result = self.cursor.fetchall()

        return result


class PartitionFeature(BasePartitionFeature):
    decorate = ('save',)

    @property
    def model_meta(self):
        meta = self.model_cls._meta

        try:
            if self.model_obj is None:
                column_value = None
            else:
                field = meta.get_field(self.options['column'])
                column_value = field.pre_save(self.model_obj, self.model_obj.pk is None)
        except KeyError as key:
            raise OptionNotSetError(model=self.model_cls.__name__, current=key)
        except FieldDoesNotExist:
            raise PartitionColumnError(
                model=self.model_cls.__name__,
                current=self.options['column'],
                allowed=meta.get_all_field_names())

        return {
            'table': meta.db_table,
            'pk': meta.pk.column,
            'dialect': connection.vendor,
            'column_value': column_value,
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
