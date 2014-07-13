from pony.orm import *
from architect.orms.pony.mixins import PartitionableMixin

db = Database('postgres', user='postgres', password='', host='localhost', database='architect')


class Document(PartitionableMixin, db.Entity):
    name = Required(unicode)
    created = Required(datetime.datetime)
    composite_key(name, created)

    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = 'day'
        partition_column = 'created'

db.generate_mapping(create_tables=True)
