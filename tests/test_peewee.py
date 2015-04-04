import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('PEEWEE'):
    raise unittest.SkipTest('Not a Peewee build')

from .models.peewee import *


class BasePeeweePartitionTestCase(object):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.peewee']
        with capture() as (out, _):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ.get('DB') == 'sqlite', 'Not a SQLite build')
class SQLitePeeweePartitionTestCase(BasePeeweePartitionTestCase, unittest.TestCase):
    def test_dummy(self):
        object1 = RangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateDay.raw(
            'SELECT * FROM test_rangedateday WHERE id = ?', object1.id))[0]

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ.get('DB') == 'postgresql', 'Not a PostgreSQL build')
class PostgresqlPeeweePartitionTestCase(BasePeeweePartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateDay.raw('SELECT * FROM test_rangedateday_y2014d105 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateWeek.raw('SELECT * FROM test_rangedateweek_y2014w16 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateMonth.raw('SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateYear.raw('SELECT * FROM test_rangedateyear_y2014 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ.get('DB') == 'mysql', 'Not a MySQL build')
class MysqlPeeweePartitionTestCase(BasePeeweePartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateDay.raw(
            'SELECT * FROM test_rangedateday WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateWeek.raw(
            'SELECT * FROM test_rangedateweek WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateMonth.raw(
            'SELECT * FROM test_rangedatemonth WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateYear.raw(
            'SELECT * FROM test_rangedateyear WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)
