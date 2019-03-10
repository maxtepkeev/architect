from __future__ import absolute_import

import os
import sys

from django.conf import settings

databases = {
    'sqlite': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'},
    'pgsql': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': 'architect', 'USER': 'postgres'},
    'mysql': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'architect', 'USER': 'root'}
}

test_databases = databases.keys() if os.environ['DB'] == 'all' else [os.environ['DB']]
Router = type('Router', (object,), {
    'allow_migrate': lambda self, db, *args, **hints: hints.get('model', args[0]).db == db,  # Django 1.7 model args[0]
    'allow_syncdb': lambda self, db, model: model.db == db,  # Django <= 1.6
    'db_for_read': lambda self, model, **hints: model.db,
    'db_for_write': lambda self, model, **hints: model.db,
})

settings.configure(
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=('test',),
    DATABASE_ROUTERS=['{0}.Router'.format(__name__)],
    DATABASES=dict(default={}, **databases),
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

for database in test_databases:
    dbname = database.capitalize()

    # Generation of entities for date range partitioning
    for item in ('day', 'week', 'month', 'year'):
        class Meta(object):
            app_label = 'test'
            db_table = 'TEST_rangedate{0}'.format(item)

        name = '{0}RangeDate{1}'.format(dbname, item.capitalize())
        partition = install('partition', type='range', subtype='date', constraint=item, column='created')

        locals()[name] = partition(type(name, (models.Model,), {
            '__module__': 'test.models',
            'name': models.CharField(max_length=255),
            'created': models.DateTimeField(null=True),
            'Meta': Meta,
            'db': database,
        }))

    if database == 'pgsql':
        # Generation of entities for integer range partitioning
        for item in ('2', '5'):
            class Meta(object):
                app_label = 'test'
                db_table = 'TEST_rangeinteger{0}'.format(item)

            name = '{0}RangeInteger{1}'.format(dbname, item)
            partition = install('partition', type='range', subtype='integer', constraint=item, column='num')

            locals()[name] = partition(type(name, (models.Model,), {
                '__module__': 'test.models',
                'name': models.CharField(max_length=255),
                'num': models.IntegerField(null=True),
                'Meta': Meta,
                'db': database,
            }))

        # Generation of entities for string range partitioning
        for subtype in ('string_firstchars', 'string_lastchars'):
            for item in ('2', '5'):
                class Meta(object):
                    app_label = 'test'
                    db_table = 'TEST_range{0}{1}'.format(subtype, item)

                name = '{0}Range{1}{2}'.format(dbname, ''.join(s.capitalize() for s in subtype.split('_')), item)
                partition = install('partition', type='range', subtype=subtype, constraint=item, column='title')

                locals()[name] = partition(type(name, (models.Model,), {
                    '__module__': 'test.models',
                    'name': models.CharField(max_length=255),
                    'title': models.CharField(max_length=255, null=True),
                    'Meta': Meta,
                    'db': database,
                }))

    management.call_command(command, database=database, run_syncdb=True, verbosity=0, interactive=False)
