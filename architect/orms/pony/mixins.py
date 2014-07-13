from pony.orm.core import db_session, rollback, Optional, TransactionRolledBack

from architect.orms import BasePartitionableMixin
from architect.exceptions import PartitionColumnError


class PartitionableMixin(BasePartitionableMixin):
    """Pony ORM partitionable mixin"""

    @property
    def model_meta(self):
        """Returns model meta attributes under common names"""
        try:
            column_value = getattr(self, self.PartitionableMeta.partition_column)
        except TransactionRolledBack:
            column_value = None
        except AttributeError:
            raise PartitionColumnError(
                model=self.__class__.__name__,
                current=self.PartitionableMeta.partition_column,
                allowed=self._columns_
            )

        return {
            'table': self._table_,
            'pk': self._pk_columns_,
            'database': self._database_.provider.dialect.lower(),
            'column_value': column_value,
        }

    def execute_raw_sql(self, sql):
        """Executes given SQL"""
        with db_session:
            return self._database_._exec_sql(sql)

    @classmethod
    def get_empty_instance(cls, dsn=None):
        """Returns empty model instance"""
        if cls._database_.schema is None:
            cls._database_.generate_mapping()

        if cls._pk_is_composite_:
            cls._pk_is_composite_ = False

        with db_session:
            for column in cls._columns_without_pk_:
                getattr(cls, column).__class__ = Optional

            model = cls()
            rollback()
            return model

    def _save_(self, *args, **kwargs):
        """Checks if partition exists and creates it if needed before saving model instance"""
        partition = self.get_partition()

        if not partition.exists():
            partition.create()

        super(PartitionableMixin, self)._save_(*args, **kwargs)
