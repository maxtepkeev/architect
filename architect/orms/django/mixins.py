from django.db import connection, transaction
from django.db.models.fields import FieldDoesNotExist

from architect.orms import BasePartitionableMixin
from architect.exceptions import PartitionColumnError


class PartitionableMixin(BasePartitionableMixin):
    """Django ORM partitionable mixin"""

    @property
    def model_meta(self):
        """Returns model meta attributes under common names"""
        try:
            column_value = self._meta.get_field(self.PartitionableMeta.partition_column).pre_save(self, self.pk is None)
        except FieldDoesNotExist:
            raise PartitionColumnError(
                model=self.__class__.__name__,
                current=self.PartitionableMeta.partition_column,
                allowed=self._meta.get_all_field_names()
            )

        return {
            'table': self._meta.db_table,
            'pk': self._meta.pk.name,
            'database': connection.vendor,
            'column_value': column_value,
        }

    def execute_raw_sql(self, sql):
        """Executes given SQL"""
        try:
            autocommit = transaction.atomic  # Django >= 1.6
        except AttributeError:
            autocommit = transaction.commit_on_success  # Django <= 1.5

        with autocommit():
            return connection.cursor().execute(sql)

    @classmethod
    def get_empty_instance(cls, dsn=None):
        """Returns empty model instance"""
        return cls()

    def save(self, *args, **kwargs):
        """Checks if partition exists and creates it if needed before saving model instance"""
        partition = self.get_partition()

        if not partition.exists():
            partition.create()

        super(PartitionableMixin, self).save(*args, **kwargs)
