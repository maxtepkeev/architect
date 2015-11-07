from __future__ import absolute_import

import os

from peewee import *
from architect import install

databases = {
    'sqlite': SqliteDatabase(':memory:'),
    'pgsql': PostgresqlDatabase('architect', user='postgres'),
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
    partition = install('partition', type='range', subtype='date', constraint=item, column='created')

    locals()[name] = partition(type(name, (Model,), {
        'name': CharField(),
        'created': DateTimeField(null=True),
        'Meta': Meta,
    }))

    locals()[name].create_table(True)

if os.environ.get('DB') in ('pgsql', 'postgresql'):
    # Generation of entities for integer range partitioning
    for item in ('2', '5'):
        class Meta(object):
            database = db
            db_table = 'test_rangeinteger{0}'.format(item)

        name = 'RangeInteger{0}'.format(item)
        partition = install('partition', type='range', subtype='integer', constraint=item, column='num')

        locals()[name] = partition(type(name, (Model,), {
            'name': CharField(),
            'num': IntegerField(null=True),
            'Meta': Meta,
        }))

        locals()[name].create_table(True)

    # Generation of entities for string range partitioning
    for subtype in ('string_firstchars', 'string_lastchars'):
        for item in ('2', '5'):
            class Meta(object):
                database = db
                db_table = 'test_range{0}{1}'.format(subtype, item)

            name = 'Range{0}{1}'.format(''.join(s.capitalize() for s in subtype.split('_')), item)
            partition = install('partition', type='range', subtype=subtype, constraint=item, column='title')

            locals()[name] = partition(type(name, (Model,), {
                'name': CharField(),
                'title': CharField(null=True),
                'Meta': Meta,
            }))

            locals()[name].create_table(True)
