class BasePartition(object):
    """Base partition class. All databases should inherit from it"""
    def __init__(self, **kwargs):
        self.column_value = kwargs['column_value']
        self.column_name = kwargs['partition_column']
        self.execute = kwargs['execute']
        self.model = kwargs['model']
        self.table = kwargs['table']
        self.pks = kwargs['pk'] if isinstance(kwargs['pk'], list) else [kwargs['pk']]

    def prepare(self):
        """Prepares everything that is needed to initialize partitioning"""
        raise NotImplementedError('Method "prepare" not implemented in: {0}'.format(self.__class__.__name__))

    def exists(self):
        """Checks if partition exists"""
        raise NotImplementedError('Method "exists" not implemented in: {0}'.format(self.__class__.__name__))

    def create(self):
        """Creates new partition"""
        raise NotImplementedError('Method "create" not implemented in: {0}'.format(self.__class__.__name__))

    def _get_name(self):
        """Defines name for a new partition"""
        raise NotImplementedError('Method "_get_name" not implemented in: {0}'.format(self.__class__.__name__))

    def _get_partition_function(self):
        """Contains a partition function that is used to create new partitions at database level"""
        raise NotImplementedError(
            'Method "_get_partition_function" not implemented in: {0}'.format(self.__class__.__name__)
        )
