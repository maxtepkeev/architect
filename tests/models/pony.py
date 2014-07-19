from __future__ import absolute_import

import os
import datetime

from pony.orm import *
from architect.orms.pony.mixins import PartitionableMixin

databases = {
    'postgresql': Database('postgres', user='postgres', password='', host='localhost', database='architect'),
    'mysql': Database('mysql', user='root', host='localhost', database='architect')
}

db = databases[os.environ.get('DB')]

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
