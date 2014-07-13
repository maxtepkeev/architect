from architect.exceptions import DatabaseError, PartitionTypeError


class BasePartitionableMixin(object):
    """Base partitionable mixin class. All orms should inherit from it"""

    def get_database(self):
        """Returns requested database module"""
        try:
            return __import__('architect.databases.{0}'.format(self.model_meta['database']), fromlist='*')
        except ImportError:
            import os
            import pkgutil
            raise DatabaseError(
                current=self.model_meta['database'],
                allowed=[name for _, name, is_package in pkgutil.iter_modules(
                    [os.path.join(os.path.dirname(__file__), '..', 'databases')]) if is_package]
            )

    def get_partition(self):
        """Returns requested partition type object to work with"""
        meta = self.PartitionableMeta

        try:
            return getattr(self.get_database().partition, '{0}Partition'.format(meta.partition_type.capitalize()))(
                execute=self.execute_raw_sql,
                model=self.__class__.__name__,
                **dict(((k, v) for k, v in meta.__dict__.items() if not k.startswith('__')), **self.model_meta)
            )
        except AttributeError:
            import re
            raise PartitionTypeError(
                model=self.__class__.__name__,
                database=self.model_meta['database'],
                current=meta.partition_type,
                allowed=[c.replace('Partition', '').lower() for c in dir(
                    self.get_database().partition) if re.match('\w+Partition', c) is not None and 'Base' not in c]
            )

    @property
    def model_meta(self):
        """Returns dictionary of model meta attributes under common names"""
        raise NotImplementedError('Property "model_meta" not implemented in: {0}'.format(self.__class__.__name__))

    def execute_raw_sql(self, sql):
        """Executes given SQL"""
        raise NotImplementedError('Method "execute_raw_sql" not implemented in: {0}'.format(self.__class__.__name__))

    @classmethod
    def get_empty_instance(cls, dsn=None):
        """Returns empty model instance"""
        raise NotImplementedError('Method "get_empty_instance" not implemented in: {0}'.format(cls.__name__))

    class PartitionableMeta:
        """Container for partition settings"""
        partition_type = 'None'
        partition_subtype = 'None'
        partition_range = 'None'
        partition_column = 'None'
