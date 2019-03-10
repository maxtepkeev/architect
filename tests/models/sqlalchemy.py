from __future__ import absolute_import

import os

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from architect import install

databases = {
    'sqlite': 'sqlite://',
    'pgsql': 'postgresql+psycopg2://postgres@localhost/architect',
    'mysql': 'mysql+pymysql://root@localhost/architect'
}

test_databases = databases.keys() if os.environ['DB'] == 'all' else [os.environ['DB']]

for database in test_databases:
    dbname = database.capitalize()
    Base = declarative_base()
    locals()['{0}_engine'.format(database)] = engine = create_engine(databases[database])

    # Generation of entities for date range partitioning
    for item in ('day', 'week', 'month', 'year'):
        name = '{0}RangeDate{1}'.format(dbname, item.capitalize())
        partition = install(
            'partition', type='range', subtype='date', constraint=item, column='created', db=engine.url)

        locals()[name] = partition(type(name, (Base,), {
            '__tablename__': 'TEST_rangedate{0}'.format(item),
            'id': Column(Integer, primary_key=True),
            'name': Column(String(length=255)),
            'created': Column(DateTime, nullable=True)
        }))

    if database == 'pgsql':
        # Generation of entities for integer range partitioning
        for item in ('2', '5'):
            name = '{0}RangeInteger{1}'.format(dbname, item)
            partition = install(
                'partition', type='range', subtype='integer', constraint=item, column='num', db=engine.url)

            locals()[name] = partition(type(name, (Base,), {
                '__tablename__': 'TEST_rangeinteger{0}'.format(item),
                'id': Column(Integer, primary_key=True),
                'name': Column(String(length=255)),
                'num': Column(Integer, nullable=True)
            }))

        # Generation of entities for string range partitioning
        for subtype in ('string_firstchars', 'string_lastchars'):
            for item in ('2', '5'):
                name = '{0}Range{1}{2}'.format(dbname, ''.join(s.capitalize() for s in subtype.split('_')), item)
                partition = install(
                    'partition', type='range', subtype=subtype, constraint=item, column='title', db=engine.url)

                locals()[name] = partition(type(name, (Base,), {
                    '__tablename__': 'TEST_range{0}{1}'.format(subtype, item),
                    'id': Column(Integer, primary_key=True),
                    'name': Column(String(length=255)),
                    'title': Column(String(length=255), nullable=True)
                }))

    Base.metadata.create_all(engine)
