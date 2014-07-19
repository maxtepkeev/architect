from peewee import CompositeKey

from architect.orms import BasePartitionableMixin
from architect.exceptions import PartitionColumnError


class PartitionableMixin(BasePartitionableMixin):
    """Peewee ORM partitionable mixin"""

    @property
    def model_meta(self):
        """Returns model meta attributes under common names"""
        try:
            column_value = getattr(self, self.PartitionableMeta.partition_column)
        except AttributeError:
            raise PartitionColumnError(
                model=self.__class__.__name__,
                current=self.PartitionableMeta.partition_column,
                allowed=self._meta.get_field_names()
            )

        pk = self._meta.primary_key

        return {
            'table': self._meta.db_table,
            'pk': list(pk.field_names) if isinstance(pk, CompositeKey) else pk.name,
            'dialect': self._meta.database.__class__.__name__.lower().replace('database', ''),
            'column_value': column_value,
        }

    def get_cursor(self):
        """Returns database cursor"""
        return self._meta.database.get_cursor()

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
