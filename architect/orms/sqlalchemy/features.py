"""
Defines features for the SQLAlchemy ORM.
"""

from sqlalchemy import create_engine, event
from sqlalchemy.exc import ArgumentError

from ..bases import BasePartitionFeature, BaseOperationFeature
from ...exceptions import OptionNotSetError, OptionValueError


class ConnectionMixin(object):
    """
    Because SQLAlchemy doesn't provide a way to get a database connection from
    a model we have to ask for the DSN and instantiate a connection ourselves.
    """
    @property
    def connection(self):
        if self.model_cls.metadata.is_bound():
            return self.model_cls.metadata.bind

        try:
            return create_engine(self.options['db'])
        except KeyError as key:
            raise OptionNotSetError(model=self.model_cls.__name__, current=key)
        except ArgumentError as e:
            raise OptionValueError(model=self.model_cls.__name__, current=self.options['db'], option='db', cause=e)


class OperationFeature(ConnectionMixin, BaseOperationFeature):
    def execute(self, sql, autocommit=True):
        return self.connection.execution_options(autocommit=autocommit).execute(sql.replace('%', '%%'))


class PartitionFeature(ConnectionMixin, BasePartitionFeature):
    @property
    def model_meta(self):
        return {
            'table': self.model_cls.__table__.name,
            'pk': self.model_cls.__table__.primary_key.columns.keys(),
            'dialect': self.connection.dialect.name,
            'column_value': self._column_value(self.model_cls.__table__.columns.keys()),
        }

    @staticmethod
    def register_hooks(model):
        """
        Registers hooks for a model.

        :param class model: (required). A model to work with.
        """
        def before_insert(*args):
            partition = args[2].architect.partition.get_partition()

            if not partition.exists():
                partition.create()

        event.listen(model, 'before_insert', before_insert)
