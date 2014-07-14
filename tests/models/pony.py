from __future__ import absolute_import

import datetime

from pony.orm import *
from architect.orms.pony.mixins import PartitionableMixin

db = Database('postgres', user='postgres', password='', host='localhost', database='architect')

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = item
        partition_column = 'created'

    name = 'RangeDate{0}'.format(item.capitalize())

    locals()[name] = type(name, (PartitionableMixin, db.Entity), {
        '_table_': 'test_rangedate{0}'.format(item),
        'name': Required(unicode),
        'created': Required(datetime.datetime),
        'PartitionableMeta': PartitionableMeta
    })

db.generate_mapping(create_tables=True)
