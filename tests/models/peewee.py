from __future__ import absolute_import

import os

from peewee import *
from architect import install
from architect.orms.peewee.features import names

databases = {
    'sqlite': SqliteDatabase(':memory:'),
    'pgsql': PostgresqlDatabase('architect', user='postgres'),
    'mysql': MySQLDatabase('architect', user='root')
}

test_databases = databases.keys() if os.environ['DB'] == 'all' else [os.environ['DB']]

for database in test_databases:
    dbname = database.capitalize()
    db = databases[database]

    # Generation of entities for date range partitioning
    for item in ('day', 'week', 'month', 'year'):
        class Meta(object):
            database = db
        setattr(Meta, names['meta_table'], 'TEST_rangedate{0}'.format(item))

        name = '{0}RangeDate{1}'.format(dbname, item.capitalize())
        partition = install('partition', type='range', subtype='date', constraint=item, column='created')

        locals()[name] = partition(type(name, (Model,), {
            'name': CharField(),
            'created': DateTimeField(null=True),
            'Meta': Meta,
        }))

        locals()[name].create_table(True)

    if database == 'pgsql':
        # Generation of entities for integer range partitioning
        for item in ('2', '5'):
            class Meta(object):
                database = db
            setattr(Meta, names['meta_table'], 'TEST_rangeinteger{0}'.format(item))

            name = '{0}RangeInteger{1}'.format(dbname, item)
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
                setattr(Meta, names['meta_table'], 'TEST_range{0}{1}'.format(subtype, item))

                name = '{0}Range{1}{2}'.format(dbname, ''.join(s.capitalize() for s in subtype.split('_')), item)
                partition = install('partition', type='range', subtype=subtype, constraint=item, column='title')

                locals()[name] = partition(type(name, (Model,), {
                    'name': CharField(),
                    'title': CharField(null=True),
                    'Meta': Meta,
                }))

                locals()[name].create_table(True)
