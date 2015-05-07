"""
Defines base classes used in orms module.
"""

from .registry import Registrar
from ..compat import with_metaclass
from ..databases.utilities import get_database
from ..exceptions import (
    PartitionTypeError,
    OptionNotSetError,
    PartitionColumnError
)


class BaseFeature(with_metaclass(Registrar)):
    """
    Each feature is installed into the model using an "install" decorator. This class defines a
    common set of attributes and methods which is needed for a feature to be properly installed.
    """
    orm = None         #: which orm this feature belongs to
    name = None        #: name that will be used to access this feature
    decorate = ()      #: model methods that should be decorated by feature decorators
    dependencies = ()  #: features that this feature depends on

    def __init__(self, model_obj, model_cls, **options):
        """
        :param object model_obj: (required). Model instance object to work with.
        :param class model_cls: (required). Model class to work with.
        :param dictionary options: (optional). Feature options if any.
        """
        self.model_obj = model_obj
        self.model_cls = model_cls
        self.options = options


class BaseOperationFeature(BaseFeature):
    """
    Sometimes there is a need to execute raw SQL statements, unfortunately different ORMs provide
    different APIs to work with raw SQL. This feature creates an abstraction layer to execute raw
    SQL statements which will work with any supported ORM.
    """
    name = 'operation'

    def execute(self, sql, autocommit=True):
        """
        Executes raw SQL for write operations.

        :param string sql: (required). SQL statement to execute.
        :param boolean autocommit: (optional). Turns autocommit on/off.
        """
        raise NotImplementedError('Method "execute" not implemented in: {0}'.format(self.__class__.__name__))

    def select_one(self, sql):
        """
        Executes raw SQL for read operations and returns a single result.

        :param string sql: (required). SQL statement to execute.
        """
        cursor = self.execute(sql)
        result = cursor.fetchone()
        return result[0] if result is not None else result

    def select_all(self, sql, as_dict=False):
        """
        Executes raw SQL for read operations and returns all results.

        :param string sql: (required). SQL statement to execute.
        :param boolean as_dict: (optional). Whether to return result as dict or as a list of tuples.
        """
        cursor = self.execute(sql)

        if as_dict:
            result = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        else:
            result = cursor.fetchall()

        return result


class BasePartitionFeature(BaseFeature):
    """
    Implements table partitioning functionality for the model.
    """
    name = 'partition'
    dependencies = ('operation',)

    def get_partition(self):
        """
        Returns partition type object to work with depending on the given partition options.
        """
        database = get_database(self.model_meta['dialect'])

        try:
            cls_name = '{0}Partition'.format(self.options['type'].capitalize())
            return getattr(database.partition, cls_name)(self.model_cls, **dict(self.options, **self.model_meta))
        except KeyError as key:
            raise OptionNotSetError(model=self.model_cls.__name__, current=key)
        except AttributeError:
            import re
            raise PartitionTypeError(
                model=self.model_cls.__name__,
                dialect=self.model_meta['dialect'],
                current=self.options['type'],
                allowed=[cls.replace('Partition', '').lower() for cls in dir(
                    database.partition) if re.match('\w+Partition', cls) is not None and 'Base' not in cls])

    @property
    def model_meta(self):
        """
        Returns dictionary of model meta attributes needed for partitioning under common names.
        """
        raise NotImplementedError('Property "model_meta" not implemented in: {0}'.format(self.__class__.__name__))

    def _column_value(self, allowed_columns):
        """
        Returns current value for the specified partition column.

        :param list allowed_columns: (required). Names of valid columns for current model.
        """
        try:
            return None if self.model_obj is None else getattr(self.model_obj, self.options['column'])
        except KeyError as key:
            raise OptionNotSetError(model=self.model_cls.__name__, current=key)
        except AttributeError:
            raise PartitionColumnError(
                model=self.model_cls.__name__,
                current=self.options['column'],
                allowed=allowed_columns)
