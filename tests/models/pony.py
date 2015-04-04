from __future__ import absolute_import

import os
import datetime

from pony.orm import *
from architect import install

databases = {
    'sqlite': {'type': 'sqlite', 'args': (':memory:',), 'kwargs': {}},
    'postgresql': {'type': 'postgres', 'args': (), 'kwargs': {'user': 'postgres', 'database': 'architect'}},
    'mysql': {'type': 'mysql', 'args': (), 'kwargs': {'user': 'root', 'database': 'architect'}}
}

current = os.environ.get('DB')
db = Database(databases[current].pop('type'), *databases[current]['args'], **databases[current]['kwargs'])

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    name = 'RangeDate{0}'.format(item.capitalize())
    partition = install('partition', type='range', subtype='date', range=item, column='created')

    locals()[name] = partition(type(name, (db.Entity,), {
        '_table_': 'test_rangedate{0}'.format(item),
        'name': Required(unicode),
        'created': Required(datetime.datetime),
    }))

db.generate_mapping(create_tables=True)
