from __future__ import absolute_import

import os

from peewee import *
from architect import install

databases = {
    'sqlite': SqliteDatabase(':memory:'),
    'postgresql': PostgresqlDatabase('architect', user='postgres'),
    'mysql': MySQLDatabase('architect', user='root')
}

db = databases[os.environ.get('DB')]

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class Meta(object):
        database = db
        db_table = 'test_rangedate{0}'.format(item)

    name = 'RangeDate{0}'.format(item.capitalize())
    partition = install('partition', type='range', subtype='date', range=item, column='created')

    locals()[name] = partition(type(name, (Model,), {
        'name': CharField(),
        'created': DateTimeField(),
        'Meta': Meta,
    }))

    locals()[name].create_table(True)
