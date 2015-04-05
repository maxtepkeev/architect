from __future__ import absolute_import

import os
import sys

from django.conf import settings

databases = {
    'sqlite': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'},
    'postgresql': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'architect', 'USER': 'postgres'},
    'mysql': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'architect', 'USER': 'root'}
}

settings.configure(
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=('test',),
    DATABASES={'default': databases[os.environ.get('DB')]}
)

# We don't have a real app with models, so we have to fake it
sys.modules['test.models'] = type('test.models', (object,), {
    '__dict__': '',
    '__file__': '',
    '__loader__': '',
    '__spec__': ''
})

from django.db import models
from django.core import management
from architect import install

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class Meta(object):
        app_label = 'test'
        db_table = 'test_rangedate{0}'.format(item)

    name = 'RangeDate{0}'.format(item.capitalize())
    partition = install('partition', type='range', subtype='date', range=item, column='created')

    locals()[name] = partition(type(name, (models.Model,), {
        '__module__': 'test.models',
        'name': models.CharField(max_length=255),
        'created': models.DateTimeField(),
        'Meta': Meta,
    }))

# Django >= 1.7 needs this
try:
    from django import setup
    setup()
    command = 'migrate'
except ImportError:
    command = 'syncdb'

management.call_command(command, verbosity=0, interactive=False)
