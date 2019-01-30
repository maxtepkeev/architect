from __future__ import absolute_import

import os
import datetime

from pony.orm import *
from architect import install

databases = {
    'sqlite': {'type': 'sqlite', 'args': (':memory:',), 'kwargs': {}},
    'pgsql': {'type': 'postgres', 'args': (), 'kwargs': {'user': 'postgres', 'database': 'architect'}},
    'mysql': {'type': 'mysql', 'args': (), 'kwargs': {'user': 'root', 'database': 'architect'}}
}

test_databases = databases.keys() if os.environ['DB'] == 'all' else [os.environ['DB']]

for database in test_databases:
    dbname = database.capitalize()
    db = Database(databases[database].pop('type'), *databases[database]['args'], **databases[database]['kwargs'])

    # Generation of entities for date range partitioning
    for item in ('day', 'week', 'month', 'year'):
        for return_null in (True, False):
            name = '{0}RangeDate{1}{2}'.format(dbname, item.capitalize(), 'ReturnNULL' if return_null else '')
            partition = install('partition', type='range', subtype='date', constraint=item, column='created', return_null=return_null)

            locals()[name] = partition(type(name, (db.Entity,), {
                '_table_': 'test_rangedate{0}{1}'.format(item, '_return_null' if return_null else ''),
                'name': Required(unicode),
                'created': Optional(datetime.datetime, nullable=True),
            }))

    if database == 'pgsql':
        # Generation of entities for integer range partitioning
        for item in ('2', '5'):
            for return_null in (True, False):
                name = '{0}RangeInteger{1}{2}'.format(dbname, item, 'ReturnNULL' if return_null else '')
                partition = install('partition', type='range', subtype='integer', constraint=item, column='num', return_null=return_null)

                locals()[name] = partition(type(name, (db.Entity,), {
                    '_table_': 'test_rangeinteger{0}{1}'.format(item, '_return_null' if return_null else ''),
                    'name': Required(unicode),
                    'num': Optional(int, nullable=True)
                }))

        # Generation of entities for string range partitioning
        for subtype in ('string_firstchars', 'string_lastchars'):
            for item in ('2', '5'):
                for return_null in (True, False):
                    name = '{0}Range{1}{2}{3}'.format(dbname, ''.join(s.capitalize() for s in subtype.split('_')), item, 'ReturnNULL' if return_null else '')
                    partition = install('partition', type='range', subtype=subtype, constraint=item, column='title', return_null=return_null)

                    locals()[name] = partition(type(name, (db.Entity,), {
                        '_table_': 'test_range{0}{1}{2}'.format(subtype, item, '_return_null' if return_null else ''),
                        'name': Required(unicode),
                        'title': Optional(unicode, nullable=True),
                    }))

    db.generate_mapping(create_tables=True)
