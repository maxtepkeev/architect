from __future__ import absolute_import

import os
import sys

from django.conf import settings

databases = {
    'postgresql': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'architect', 'USER': 'postgres'},
    'mysql': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'architect', 'USER': 'root'}
}

settings.configure(
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=('test',),
    DATABASES={'default': databases[os.environ.get('DB')]}
)

# We don't have a real app with models, so we have to fake it
sys.modules['test.models'] = type('test.models', (object,), {'__dict__': '', '__file__': ''})

from django.db import models
from django.core import management
from architect.orms.django.mixins import PartitionableMixin

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class Meta:
        app_label = 'test'
        db_table = 'test_rangedate{0}'.format(item)

    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'date'
        partition_range = item
        partition_column = 'created'

    name = 'RangeDate{0}'.format(item.capitalize())

    locals()[name] = type(name, (PartitionableMixin, models.Model), {
        '__module__': 'test.models',
        'name': models.CharField(max_length=255),
        'created': models.DateTimeField(),
        'Meta': Meta,
        'PartitionableMeta': PartitionableMeta
    })

# Generation of entities for bigint range partitioning
for item in ('1', '5', '10', '100'):
    class Meta:
        app_label = 'test'
        db_table = 'test_rangebigint{0}'.format(item)

    class PartitionableMeta:
        partition_type = 'range'
        partition_subtype = 'bigint'
        partition_range = item
        partition_column = 'created'

    name = 'RangeBigint{0}'.format(item)

    locals()[name] = type(name, (PartitionableMixin, models.Model), {
        '__module__': 'test.models',
        'name': models.CharField(max_length=255),
        'created': models.BigIntegerField(),
        'Meta': Meta,
        'PartitionableMeta': PartitionableMeta
    })

# Django >= 1.7 needs this
try:
    from django import setup
    setup()
except ImportError:
    pass

management.call_command('syncdb', interactive=False)
