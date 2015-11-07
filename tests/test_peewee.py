"""
Tests Peewee specific behaviour.
"""

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


@unittest.skipUnless(os.environ.get('DB') in ('pgsql', 'postgresql'), 'Not a PostgreSQL build')
class PostgresqlPeeweePartitionTestCase(BasePeeweePartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateDay.raw('SELECT * FROM test_rangedateday_y2014d105 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        object1 = RangeDateDay.create(name='foo')
        object2 = list(RangeDateDay.raw('SELECT * FROM test_rangedateday_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateWeek.raw('SELECT * FROM test_rangedateweek_y2014w16 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        object1 = RangeDateWeek.create(name='foo')
        object2 = list(RangeDateWeek.raw('SELECT * FROM test_rangedateweek_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateMonth.raw('SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        object1 = RangeDateMonth.create(name='foo')
        object2 = list(RangeDateMonth.raw('SELECT * FROM test_rangedatemonth_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = list(RangeDateYear.raw('SELECT * FROM test_rangedateyear_y2014 WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        object1 = RangeDateYear.create(name='foo')
        object2 = list(RangeDateYear.raw('SELECT * FROM test_rangedateyear_null WHERE id = %s', object1.id))[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        object1 = RangeInteger2.create(name='foo', num=3)
        object2 = list(RangeInteger2.raw('SELECT * FROM test_rangeinteger2_3_4 WHERE id = %s', object1.id))[0]
        object3 = RangeInteger5.create(name='foo', num=3)
        object4 = list(RangeInteger5.raw('SELECT * FROM test_rangeinteger5_1_5 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        object1 = RangeInteger2.create(name='foo', num=0)
        object2 = list(RangeInteger2.raw('SELECT * FROM test_rangeinteger2_0 WHERE id = %s', object1.id))[0]
        object3 = RangeInteger5.create(name='foo', num=0)
        object4 = list(RangeInteger5.raw('SELECT * FROM test_rangeinteger5_0 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        object1 = RangeInteger2.create(name='foo', num=-3)
        object2 = list(RangeInteger2.raw('SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = %s', object1.id))[0]
        object3 = RangeInteger5.create(name='foo', num=-3)
        object4 = list(RangeInteger5.raw('SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        object1 = RangeInteger2.create(name='foo')
        object2 = list(RangeInteger2.raw('SELECT * FROM test_rangeinteger2_null WHERE id = %s', object1.id))[0]
        object3 = RangeInteger5.create(name='foo')
        object4 = list(RangeInteger5.raw('SELECT * FROM test_rangeinteger5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        object1 = RangeStringFirstchars2.create(name='foo', title='abcdef')
        object2 = list(RangeStringFirstchars2.raw(
            'SELECT * FROM test_rangestring_firstchars2_ab WHERE id = %s', object1.id))[0]
        object3 = RangeStringFirstchars5.create(name='foo', title='abcdef')
        object4 = list(RangeStringFirstchars5.raw(
            'SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        object1 = RangeStringFirstchars2.create(name='foo', title=';<abcdef')
        object2 = list(RangeStringFirstchars2.raw(
            'SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = %s', object1.id))[0]
        object3 = RangeStringFirstchars5.create(name='foo', title='ab;<cdef')
        object4 = list(RangeStringFirstchars5.raw(
            'SELECT * FROM "test_rangestring_firstchars5_ab;<c" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        object1 = RangeStringFirstchars2.create(name='foo')
        object2 = list(RangeStringFirstchars2.raw(
            'SELECT * FROM test_rangestring_firstchars2_null WHERE id = %s', object1.id))[0]
        object3 = RangeStringFirstchars5.create(name='foo')
        object4 = list(RangeStringFirstchars5.raw(
            'SELECT * FROM test_rangestring_firstchars5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        object1 = RangeStringLastchars2.create(name='foo', title='abcdef')
        object2 = list(RangeStringLastchars2.raw(
            'SELECT * FROM test_rangestring_lastchars2_ef WHERE id = %s', object1.id))[0]
        object3 = RangeStringLastchars5.create(name='foo', title='abcdef')
        object4 = list(RangeStringLastchars5.raw(
            'SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        object1 = RangeStringLastchars2.create(name='foo', title='abcd;<')
        object2 = list(RangeStringLastchars2.raw(
            'SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = %s', object1.id))[0]
        object3 = RangeStringLastchars5.create(name='foo', title='abcd;<')
        object4 = list(RangeStringLastchars5.raw(
            'SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        object1 = RangeStringLastchars2.create(name='foo')
        object2 = list(RangeStringLastchars2.raw(
            'SELECT * FROM test_rangestring_lastchars2_null WHERE id = %s', object1.id))[0]
        object3 = RangeStringLastchars5.create(name='foo')
        object4 = list(RangeStringLastchars5.raw(
            'SELECT * FROM test_rangestring_lastchars5_null WHERE id = %s', object3.id))[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


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
