from __future__ import absolute_import

from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from architect.orms.sqlalchemy.mixins import PartitionableMixin

dsn = 'postgresql+psycopg2://postgres@localhost/architect'
engine = create_engine(dsn)
Base = declarative_base()

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = item
        partition_column = 'created'

    name = 'RangeDate{0}'.format(item.capitalize())

    locals()[name] = type(name, (PartitionableMixin, Base), {
        '__tablename__': 'test_rangedate{0}'.format(item),
        'id': Column(Integer, primary_key=True),
        'name': Column(String),
        'created': Column(DateTime),
        'PartitionableMeta': PartitionableMeta
    })

Base.metadata.create_all(engine)
