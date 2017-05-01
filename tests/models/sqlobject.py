from __future__ import absolute_import

import os

from sqlobject import *
from distutils.version import LooseVersion

from architect import install

databases = {
    'sqlite': 'sqlite:/:memory:',
    'pgsql': 'postgresql://postgres@localhost/architect?driver=psycopg2',
    'mysql': 'mysql://root@localhost:3306/architect?{0}'.format(
        '' if LooseVersion(version) < LooseVersion('3.2.0') else 'driver=pymysql')
}

test_databases = databases.keys() if os.environ['DB'] == 'all' else [os.environ['DB']]

for database in test_databases:
    dbname = database.capitalize()
    connection = connectionForURI(databases[database])

    # Generation of entities for date range partitioning
    for item in ('day', 'week', 'month', 'year'):
        class sqlmeta(object):
            table = 'test_rangedate{0}'.format(item)

        name = '{0}RangeDate{1}'.format(dbname, item.capitalize())
        partition = install('partition', type='range', subtype='date', constraint=item, column='created')

        locals()[name] = partition(type(name, (SQLObject,), {
            'name': StringCol(),
            'created': DateTimeCol(default=None),
            'sqlmeta': sqlmeta,
            '_connection': connection
        }))

        locals()[name].createTable(True)

    if database == 'pgsql':
        # Generation of entities for integer range partitioning
        for item in ('2', '5'):
            class sqlmeta(object):
                table = 'test_rangeinteger{0}'.format(item)

            name = '{0}RangeInteger{1}'.format(dbname, item)
            partition = install('partition', type='range', subtype='integer', constraint=item, column='num')

            locals()[name] = partition(type(name, (SQLObject,), {
                'name': StringCol(),
                'num': IntCol(default=None),
                'sqlmeta': sqlmeta,
                '_connection': connection
            }))

            locals()[name].createTable(True)

        # Generation of entities for string range partitioning
        for subtype in ('string_firstchars', 'string_lastchars'):
            for item in ('2', '5'):
                class sqlmeta(object):
                    table = 'test_range{0}{1}'.format(subtype, item)

                name = '{0}Range{1}{2}'.format(dbname, ''.join(s.capitalize() for s in subtype.split('_')), item)
                partition = install('partition', type='range', subtype=subtype, constraint=item, column='title')

                locals()[name] = partition(type(name, (SQLObject,), {
                    'name': StringCol(),
                    'title': StringCol(default=None),
                    'sqlmeta': sqlmeta,
                    '_connection': connection
                }))

                locals()[name].createTable(True)
