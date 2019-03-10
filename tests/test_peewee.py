"""
Tests Peewee specific behaviour.
"""

import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('PEEWEE') or not os.environ.get('DB'):
    raise unittest.SkipTest('Not a Peewee build')

from .models.peewee import *


def setUpModule():
    sys.argv = ['architect', 'partition', '--module', 'tests.models.peewee']
    with capture() as (out, _):
        search = 'successfully (re)configured the database for the following models'
        assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ['DB'] in ('sqlite', 'all'), 'Not a SQLite build')
class SQLitePeeweePartitionTestCase(unittest.TestCase):
    def test_dummy(self):
        object1 = SqliteRangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(SqliteRangeDateDay.raw('SELECT * FROM TEST_rangedateday WHERE id = ?', object1.id))[0]

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ['DB'] in ('pgsql', 'all'), 'Not a PostgreSQL build')
class PostgresqlPeeweePartitionTestCase(unittest.TestCase):
    def test_range_date_day(self):
        object1 = PgsqlRangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(PgsqlRangeDateDay.raw('SELECT * FROM TEST_rangedateday_y2014d105 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        object1 = PgsqlRangeDateDay.create(name='foo')
        object2 = list(PgsqlRangeDateDay.raw('SELECT * FROM TEST_rangedateday_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = PgsqlRangeDateWeek.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(PgsqlRangeDateWeek.raw('SELECT * FROM TEST_rangedateweek_y2014w16 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        object1 = PgsqlRangeDateWeek.create(name='foo')
        object2 = list(PgsqlRangeDateWeek.raw('SELECT * FROM TEST_rangedateweek_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = PgsqlRangeDateMonth.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(PgsqlRangeDateMonth.raw(
            'SELECT * FROM TEST_rangedatemonth_y2014m04 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        object1 = PgsqlRangeDateMonth.create(name='foo')
        object2 = list(PgsqlRangeDateMonth.raw('SELECT * FROM TEST_rangedatemonth_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = PgsqlRangeDateYear.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(PgsqlRangeDateYear.raw('SELECT * FROM TEST_rangedateyear_y2014 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        object1 = PgsqlRangeDateYear.create(name='foo')
        object2 = list(PgsqlRangeDateYear.raw('SELECT * FROM TEST_rangedateyear_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        object1 = PgsqlRangeInteger2.create(name='foo', num=3)
        object2 = list(PgsqlRangeInteger2.raw('SELECT * FROM TEST_rangeinteger2_3_4 WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeInteger5.create(name='foo', num=3)
        object4 = list(PgsqlRangeInteger5.raw('SELECT * FROM TEST_rangeinteger5_1_5 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        object1 = PgsqlRangeInteger2.create(name='foo', num=0)
        object2 = list(PgsqlRangeInteger2.raw('SELECT * FROM TEST_rangeinteger2_0 WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeInteger5.create(name='foo', num=0)
        object4 = list(PgsqlRangeInteger5.raw('SELECT * FROM TEST_rangeinteger5_0 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        object1 = PgsqlRangeInteger2.create(name='foo', num=-3)
        object2 = list(PgsqlRangeInteger2.raw('SELECT * FROM TEST_rangeinteger2_m4_m3 WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeInteger5.create(name='foo', num=-3)
        object4 = list(PgsqlRangeInteger5.raw('SELECT * FROM TEST_rangeinteger5_m5_m1 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        object1 = PgsqlRangeInteger2.create(name='foo')
        object2 = list(PgsqlRangeInteger2.raw('SELECT * FROM TEST_rangeinteger2_null WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeInteger5.create(name='foo')
        object4 = list(PgsqlRangeInteger5.raw('SELECT * FROM TEST_rangeinteger5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        object1 = PgsqlRangeStringFirstchars2.create(name='foo', title='abcdef')
        object2 = list(PgsqlRangeStringFirstchars2.raw(
            'SELECT * FROM "TEST_rangestring_firstchars2_ab" WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringFirstchars5.create(name='foo', title='abcdef')
        object4 = list(PgsqlRangeStringFirstchars5.raw(
            'SELECT * FROM "TEST_rangestring_firstchars5_abcde" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        object1 = PgsqlRangeStringFirstchars2.create(name='foo', title=';<abcdef')
        object2 = list(PgsqlRangeStringFirstchars2.raw(
            'SELECT * FROM "TEST_rangestring_firstchars2_;<" WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringFirstchars5.create(name='foo', title='ab;<cdef')
        object4 = list(PgsqlRangeStringFirstchars5.raw(
            'SELECT * FROM "TEST_rangestring_firstchars5_ab;<c" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        object1 = PgsqlRangeStringFirstchars2.create(name='foo')
        object2 = list(PgsqlRangeStringFirstchars2.raw(
            'SELECT * FROM TEST_rangestring_firstchars2_null WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringFirstchars5.create(name='foo')
        object4 = list(PgsqlRangeStringFirstchars5.raw(
            'SELECT * FROM TEST_rangestring_firstchars5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        object1 = PgsqlRangeStringLastchars2.create(name='foo', title='abcdef')
        object2 = list(PgsqlRangeStringLastchars2.raw(
            'SELECT * FROM "TEST_rangestring_lastchars2_ef" WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringLastchars5.create(name='foo', title='abcdef')
        object4 = list(PgsqlRangeStringLastchars5.raw(
            'SELECT * FROM "TEST_rangestring_lastchars5_bcdef" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        object1 = PgsqlRangeStringLastchars2.create(name='foo', title='abcd;<')
        object2 = list(PgsqlRangeStringLastchars2.raw(
            'SELECT * FROM "TEST_rangestring_lastchars2_;<" WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringLastchars5.create(name='foo', title='abcd;<')
        object4 = list(PgsqlRangeStringLastchars5.raw(
            'SELECT * FROM "TEST_rangestring_lastchars5_bcd;<" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        object1 = PgsqlRangeStringLastchars2.create(name='foo')
        object2 = list(PgsqlRangeStringLastchars2.raw(
            'SELECT * FROM TEST_rangestring_lastchars2_null WHERE id = %s', object1.id))[0]
        object3 = PgsqlRangeStringLastchars5.create(name='foo')
        object4 = list(PgsqlRangeStringLastchars5.raw(
            'SELECT * FROM TEST_rangestring_lastchars5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


@unittest.skipUnless(os.environ['DB'] in ('mysql', 'all'), 'Not a MySQL build')
class MysqlPeeweePartitionTestCase(unittest.TestCase):
    def test_range_date_day(self):
        object1 = MysqlRangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(MysqlRangeDateDay.raw('SELECT * FROM TEST_rangedateday WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = MysqlRangeDateWeek.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(MysqlRangeDateWeek.raw('SELECT * FROM TEST_rangedateweek WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = MysqlRangeDateMonth.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(MysqlRangeDateMonth.raw('SELECT * FROM TEST_rangedatemonth WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = MysqlRangeDateYear.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(MysqlRangeDateYear.raw('SELECT * FROM TEST_rangedateyear WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)
