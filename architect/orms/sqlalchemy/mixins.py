from sqlalchemy import create_engine, event
from sqlalchemy.exc import ArgumentError

from architect.orms import BasePartitionableMixin
from architect.exceptions import PartitionColumnError, DsnParseError, DsnNotProvidedError


class PartitionableMixin(BasePartitionableMixin):
    """SQLAlchemy ORM partitionable mixin"""

    @property
    def model_meta(self):
        """Returns model meta attributes under common names"""
        try:
            column_value = getattr(self, self.PartitionableMeta.partition_column)
        except AttributeError:
            raise PartitionColumnError(
                model=self.__class__.__name__,
                current=self.PartitionableMeta.partition_column,
                allowed=self.__table__.columns.keys()
            )

        return {
            'table': self.__table__.name,
            'pk': self.__table__.primary_key.columns.keys(),
            'database': self.database.dialect.name,
            'column_value': column_value,
        }

    def execute_raw_sql(self, sql):
        """Executes given SQL"""
        return self.database.execution_options(autocommit=True).execute(sql)

    @classmethod
    def get_empty_instance(cls, dsn=None):
        """Returns empty model instance"""
        instance = cls()

        try:
            instance.database = create_engine(dsn)
        except AttributeError:
            raise DsnNotProvidedError()
        except ArgumentError:
            raise DsnParseError(current=dsn)

        return instance


@event.listens_for(PartitionableMixin, 'before_insert', propagate=True)
def before_insert_listener(mapper, conn, target):
    target.database = conn.engine
    partition = target.get_partition()

    if not partition.exists():
        partition.create()
