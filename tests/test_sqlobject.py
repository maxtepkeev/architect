"""
Tests SQLObject specific behaviour.
"""

import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('SQLOBJECT') or not os.environ.get('DB'):
    raise unittest.SkipTest('Not a SQLObject build')

from .models.sqlobject import *


def setUpModule():
    sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlobject']
    with capture() as (out, _):
        search = 'successfully (re)configured the database for the following models'
        assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ['DB'] in ('sqlite', 'all'), 'Not a SQLite build')
class SQLiteSqlObjectPartitionTestCase(unittest.TestCase):
    def test_dummy(self):
        object1 = SqliteRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = SqliteRangeDateDay._connection.queryOne('SELECT * FROM test_rangedateday WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])


@unittest.skipUnless(os.environ['DB'] in ('pgsql', 'all'), 'Not a PostgreSQL build')
class PostgresqlSqlObjectPartitionTestCase(unittest.TestCase):
    def test_range_date_day(self):
        object1 = PgsqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday_y2014d105 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_day_null(self):
        object1 = PgsqlRangeDateDay(name='foo')
        object2 = PgsqlRangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week(self):
        object1 = PgsqlRangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek_y2014w16 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week_null(self):
        object1 = PgsqlRangeDateWeek(name='foo')
        object2 = PgsqlRangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month(self):
        object1 = PgsqlRangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month_null(self):
        object1 = PgsqlRangeDateMonth(name='foo')
        object2 = PgsqlRangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year(self):
        object1 = PgsqlRangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear_y2014 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year_null(self):
        object1 = PgsqlRangeDateYear(name='foo')
        object2 = PgsqlRangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_integer_positive(self):
        object1 = PgsqlRangeInteger2(name='foo', num=3)
        object3 = PgsqlRangeInteger5(name='foo', num=3)
        object2 = PgsqlRangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_3_4 WHERE id = %s' % object1.id)
        object4 = PgsqlRangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_1_5 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_zero(self):
        object1 = PgsqlRangeInteger2(name='foo', num=0)
        object3 = PgsqlRangeInteger5(name='foo', num=0)
        object2 = PgsqlRangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_0 WHERE id = %s' % object1.id)
        object4 = PgsqlRangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_0 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_negative(self):
        object1 = PgsqlRangeInteger2(name='foo', num=-3)
        object3 = PgsqlRangeInteger5(name='foo', num=-3)
        object2 = PgsqlRangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = %s' % object1.id)
        object4 = PgsqlRangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_null(self):
        object1 = PgsqlRangeInteger2(name='foo')
        object3 = PgsqlRangeInteger5(name='foo')
        object2 = PgsqlRangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_null WHERE id = %s' % object1.id)
        object4 = PgsqlRangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo', title='abcdef')
        object3 = PgsqlRangeStringFirstchars5(name='foo', title='abcdef')
        object2 = PgsqlRangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars2_ab WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars_special_characters(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo', title=';<abcdef')
        object3 = PgsqlRangeStringFirstchars5(name='foo', title=';<abcdef')
        object2 = PgsqlRangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM "test_rangestring_firstchars5_;<abc" WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars_null(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo')
        object3 = PgsqlRangeStringFirstchars5(name='foo')
        object2 = PgsqlRangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars2_null WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars(self):
        object1 = PgsqlRangeStringLastchars2(name='foo', title='abcdef')
        object3 = PgsqlRangeStringLastchars5(name='foo', title='abcdef')
        object2 = PgsqlRangeStringLastchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars2_ef WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringLastchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars_special_characters(self):
        object1 = PgsqlRangeStringLastchars2(name='foo', title='abcd;<')
        object3 = PgsqlRangeStringLastchars5(name='foo', title='abcd;<')
        object2 = PgsqlRangeStringLastchars2._connection.queryOne(
            'SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringLastchars5._connection.queryOne(
            'SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars_null(self):
        object1 = PgsqlRangeStringLastchars2(name='foo')
        object3 = PgsqlRangeStringLastchars5(name='foo')
        object2 = PgsqlRangeStringLastchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars2_null WHERE id = %s' % object1.id)
        object4 = PgsqlRangeStringLastchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])


@unittest.skipUnless(os.environ['DB'] in ('mysql', 'all'), 'Not a MySQL build')
class MysqlSqlObjectPartitionTestCase(unittest.TestCase):
    def test_range_date_day(self):
        object1 = MysqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week(self):
        object1 = MysqlRangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month(self):
        object1 = MysqlRangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year(self):
        object1 = MysqlRangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])
