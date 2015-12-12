from __future__ import absolute_import

import os
import sys

from django.conf import settings

databases = {
    'sqlite': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'},
    'pgsql': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'architect', 'USER': 'postgres'},
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

# Django >= 1.7 needs this
try:
    import django
    django.setup()
    command = 'migrate'
except AttributeError:
    command = 'syncdb'

from django.db import models
from django.core import management
from architect import install

# Generation of entities for date range partitioning
for item in ('day', 'week', 'month', 'year'):
    class Meta(object):
        app_label = 'test'
        db_table = 'test_rangedate{0}'.format(item)

    name = 'RangeDate{0}'.format(item.capitalize())
    partition = install('partition', type='range', subtype='date', constraint=item, column='created')

    locals()[name] = partition(type(name, (models.Model,), {
        '__module__': 'test.models',
        'name': models.CharField(max_length=255),
        'created': models.DateTimeField(null=True),
        'Meta': Meta,
    }))

if os.environ.get('DB') in ('pgsql', 'postgresql'):
    # Generation of entities for integer range partitioning
    for item in ('2', '5'):
        class Meta(object):
            app_label = 'test'
            db_table = 'test_rangeinteger{0}'.format(item)

        name = 'RangeInteger{0}'.format(item)
        partition = install('partition', type='range', subtype='integer', constraint=item, column='num')

        locals()[name] = partition(type(name, (models.Model,), {
            '__module__': 'test.models',
            'name': models.CharField(max_length=255),
            'num': models.IntegerField(null=True),
            'Meta': Meta,
        }))

    # Generation of entities for string range partitioning
    for subtype in ('string_firstchars', 'string_lastchars'):
        for item in ('2', '5'):
            class Meta(object):
                app_label = 'test'
                db_table = 'test_range{0}{1}'.format(subtype, item)

            name = 'Range{0}{1}'.format(''.join(s.capitalize() for s in subtype.split('_')), item)
            partition = install('partition', type='range', subtype=subtype, constraint=item, column='title')

            locals()[name] = partition(type(name, (models.Model,), {
                '__module__': 'test.models',
                'name': models.CharField(max_length=255),
                'title': models.CharField(max_length=255, null=True),
                'Meta': Meta,
            }))

management.call_command(command, run_syncdb=True, verbosity=0, interactive=False)
