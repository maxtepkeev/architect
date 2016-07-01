"""
Defines features for the Django ORM.
"""

from django.conf import settings
from django.db import router, connections, transaction
from django.db.models.fields import FieldDoesNotExist
from django.db.utils import ConnectionDoesNotExist
from django.utils.functional import cached_property

from ..bases import BasePartitionFeature, BaseOperationFeature
from ...exceptions import PartitionColumnError, OptionNotSetError, OptionValueError


class ConnectionMixin(object):
    """
    Provides support for multiple database connections.
    """
    @cached_property
    def connection(self):
        db = self.options.get('db', router.db_for_write(self.model_cls))

        try:
            return connections[db].cursor()
        except ConnectionDoesNotExist as e:
            raise OptionValueError(model=self.model_cls.__name__, current=db, option='db', cause=e)


class OperationFeature(ConnectionMixin, BaseOperationFeature):
    def execute(self, sql, autocommit=True):
        if not autocommit:
            return self.connection.execute(sql)

        try:
            autocommit = transaction.atomic  # Django >= 1.6
        except AttributeError:
            # Fix for Django bug #9055
            if settings.DEBUG:
                sql = sql.replace('%', '%%')

            autocommit = transaction.commit_on_success  # Django <= 1.5

        with autocommit():
            return self.connection.execute(sql)

    def select_one(self, sql):
        self.execute(sql)
        result = self.connection.fetchone()
        return result[0] if result is not None else result

    def select_all(self, sql, as_dict=False):
        self.execute(sql)

        if as_dict:
            result = [dict(zip([c[0] for c in self.connection.description], row)) for row in self.connection.fetchall()]
        else:
            result = self.connection.fetchall()

        return result


class PartitionFeature(ConnectionMixin, BasePartitionFeature):
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
            'dialect': self.connection.db.vendor,
            'column_value': column_value,
        }

    @staticmethod
    def _decorate_save(method):
        """
        Checks if partition exists and creates it if needed before saving model instance.
        """
        def wrapper(instance, *args, **kwargs):
            feature = instance.architect.partition

            if feature.options.get('db') is not None and 'using' not in kwargs:
                kwargs['using'] = feature.options['db']

            partition = feature.get_partition()

            if not partition.exists():
                partition.create()

            method(instance, *args, **kwargs)
        return wrapper
