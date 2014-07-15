from __future__ import absolute_import

from peewee import *
from architect.orms.peewee.mixins import PartitionableMixin

db = PostgresqlDatabase('architect', user='postgres')

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class Meta:
        database = db
        db_table = 'test_rangedate{0}'.format(item)

    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = item
        partition_column = 'created'

    name = 'RangeDate{0}'.format(item.capitalize())

    locals()[name] = type(name, (PartitionableMixin, Model), {
        'name': CharField(),
        'created': DateTimeField(),
        'Meta': Meta,
        'PartitionableMeta': PartitionableMeta
    })

    locals()[name].create_table(True)
