"""
Tests SQLObject specific behaviour.
"""

import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('SQLOBJECT'):
    raise unittest.SkipTest('Not a SQLObject build')

# PyMySQL doesn't have CR module and SQLObject needs it so we have
# to fake it, see https://github.com/PyMySQL/PyMySQL/issues/336
sys.modules['MySQLdb.constants.CR'] = type('CR', (object,), {})

from .models.sqlobject import *


class BaseSqlObjectPartitionTestCase(object):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlobject']
        with capture() as (out, _):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ.get('DB') == 'sqlite', 'Not a SQLite build')
class SQLiteSqlObjectPartitionTestCase(BaseSqlObjectPartitionTestCase, unittest.TestCase):
    def test_dummy(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])


@unittest.skipUnless(os.environ.get('DB') in ('pgsql', 'postgresql'), 'Not a PostgreSQL build')
class PostgresqlSqlObjectPartitionTestCase(BaseSqlObjectPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday_y2014d105 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_day_null(self):
        object1 = RangeDateDay(name='foo')
        object2 = RangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week(self):
        object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek_y2014w16 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week_null(self):
        object1 = RangeDateWeek(name='foo')
        object2 = RangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month(self):
        object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month_null(self):
        object1 = RangeDateMonth(name='foo')
        object2 = RangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year(self):
        object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear_y2014 WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year_null(self):
        object1 = RangeDateYear(name='foo')
        object2 = RangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear_null WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_integer_positive(self):
        object1 = RangeInteger2(name='foo', num=3)
        object3 = RangeInteger5(name='foo', num=3)
        object2 = RangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_3_4 WHERE id = %s' % object1.id)
        object4 = RangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_1_5 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_zero(self):
        object1 = RangeInteger2(name='foo', num=0)
        object3 = RangeInteger5(name='foo', num=0)
        object2 = RangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_0 WHERE id = %s' % object1.id)
        object4 = RangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_0 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_negative(self):
        object1 = RangeInteger2(name='foo', num=-3)
        object3 = RangeInteger5(name='foo', num=-3)
        object2 = RangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = %s' % object1.id)
        object4 = RangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_integer_null(self):
        object1 = RangeInteger2(name='foo')
        object3 = RangeInteger5(name='foo')
        object2 = RangeInteger2._connection.queryOne(
            'SELECT * FROM test_rangeinteger2_null WHERE id = %s' % object1.id)
        object4 = RangeInteger5._connection.queryOne(
            'SELECT * FROM test_rangeinteger5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars(self):
        object1 = RangeStringFirstchars2(name='foo', title='abcdef')
        object3 = RangeStringFirstchars5(name='foo', title='abcdef')
        object2 = RangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars2_ab WHERE id = %s' % object1.id)
        object4 = RangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars_special_characters(self):
        object1 = RangeStringFirstchars2(name='foo', title=';<abcdef')
        object3 = RangeStringFirstchars5(name='foo', title=';<abcdef')
        object2 = RangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = %s' % object1.id)
        object4 = RangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM "test_rangestring_firstchars5_;<abc" WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_firstchars_null(self):
        object1 = RangeStringFirstchars2(name='foo')
        object3 = RangeStringFirstchars5(name='foo')
        object2 = RangeStringFirstchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars2_null WHERE id = %s' % object1.id)
        object4 = RangeStringFirstchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_firstchars5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars(self):
        object1 = RangeStringLastchars2(name='foo', title='abcdef')
        object3 = RangeStringLastchars5(name='foo', title='abcdef')
        object2 = RangeStringLastchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars2_ef WHERE id = %s' % object1.id)
        object4 = RangeStringLastchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars_special_characters(self):
        object1 = RangeStringLastchars2(name='foo', title='abcd;<')
        object3 = RangeStringLastchars5(name='foo', title='abcd;<')
        object2 = RangeStringLastchars2._connection.queryOne(
            'SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = %s' % object1.id)
        object4 = RangeStringLastchars5._connection.queryOne(
            'SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])

    def test_range_string_lastchars_null(self):
        object1 = RangeStringLastchars2(name='foo')
        object3 = RangeStringLastchars5(name='foo')
        object2 = RangeStringLastchars2._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars2_null WHERE id = %s' % object1.id)
        object4 = RangeStringLastchars5._connection.queryOne(
            'SELECT * FROM test_rangestring_lastchars5_null WHERE id = %s' % object3.id)

        self.assertTrue(object1.name, object2[1])
        self.assertTrue(object3.name, object4[1])


@unittest.skipUnless(os.environ.get('DB') == 'mysql', 'Not a MySQL build')
class MysqlSqlObjectPartitionTestCase(BaseSqlObjectPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateDay._connection.queryOne(
            'SELECT * FROM test_rangedateday WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_week(self):
        object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateWeek._connection.queryOne(
            'SELECT * FROM test_rangedateweek WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_month(self):
        object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateMonth._connection.queryOne(
            'SELECT * FROM test_rangedatemonth WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])

    def test_range_date_year(self):
        object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = RangeDateYear._connection.queryOne(
            'SELECT * FROM test_rangedateyear WHERE id = %s' % object1.id)

        self.assertTrue(object1.name, object2[1])
