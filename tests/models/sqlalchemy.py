from __future__ import absolute_import

import os

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from architect import install

databases = {
    'sqlite': 'sqlite://',
    'pgsql': 'postgresql+psycopg2://postgres@localhost/architect',
    'postgresql': 'postgresql+psycopg2://postgres@localhost/architect',
    'mysql': 'mysql+pymysql://root@localhost/architect'
}

dsn = databases[os.environ.get('DB')]
engine = create_engine(dsn)
Base = declarative_base()

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    name = 'RangeDate{0}'.format(item.capitalize())
    partition = install('partition', type='range', subtype='date', constraint=item, column='created', db=engine.url)

    locals()[name] = partition(type(name, (Base,), {
        '__tablename__': 'test_rangedate{0}'.format(item),
        'id': Column(Integer, primary_key=True),
        'name': Column(String(length=255)),
        'created': Column(DateTime, nullable=True)
    }))

if os.environ.get('DB') in ('pgsql', 'postgresql'):
    # Generation of entities for integer range partitioning
    for item in ('2', '5'):
        name = 'RangeInteger{0}'.format(item)
        partition = install('partition', type='range', subtype='integer', constraint=item, column='num', db=engine.url)

        locals()[name] = partition(type(name, (Base,), {
            '__tablename__': 'test_rangeinteger{0}'.format(item),
            'id': Column(Integer, primary_key=True),
            'name': Column(String(length=255)),
            'num': Column(Integer, nullable=True)
        }))

    # Generation of entities for string range partitioning
    for subtype in ('string_firstchars', 'string_lastchars'):
        for item in ('2', '5'):
            name = 'Range{0}{1}'.format(''.join(s.capitalize() for s in subtype.split('_')), item)
            partition = install('partition', type='range', subtype=subtype, constraint=item, column='title', db=engine.url)

            locals()[name] = partition(type(name, (Base,), {
                '__tablename__': 'test_range{0}{1}'.format(subtype, item),
                'id': Column(Integer, primary_key=True),
                'name': Column(String(length=255)),
                'title': Column(String(length=255), nullable=True)
            }))

Base.metadata.create_all(engine)
