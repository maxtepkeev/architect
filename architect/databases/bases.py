"""
Defines base classes used in databases module.
"""


class BasePartition(object):
    """
    Defines some common attributes and methods that are needed in all partitioning implementations.
    """
    def __init__(self, model, **meta):
        """
        :param class model: (required). A model to work with.
        :param dictionary meta: (optional). Model's meta information.
        """
        self.dialect = self.__module__.split('.')[-2]
        self.model = model
        self.database = model.architect.operation
        self.table = meta['table']
        self.column_value = meta['column_value']
        self.column_name = meta['column']
        self.pks = meta['pk'] if isinstance(meta['pk'], list) else [meta['pk']]

    def prepare(self):
        """
        Prepares everything that is needed to initialize partitioning.
        """
        raise NotImplementedError('Method "prepare" not implemented in: {0}'.format(self.__class__.__name__))

    def exists(self):
        """
        Checks if partition exists.
        """
        raise NotImplementedError('Method "exists" not implemented in: {0}'.format(self.__class__.__name__))

    def create(self):
        """
        Creates new partition.
        """
        raise NotImplementedError('Method "create" not implemented in: {0}'.format(self.__class__.__name__))
