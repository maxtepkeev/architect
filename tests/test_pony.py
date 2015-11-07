"""
Tests Pony specific behaviour.
"""

import os
import sys

from . import unittest, capture

if not os.environ.get('PONY'):
    raise unittest.SkipTest('Not a Pony build')

from pony import __version__
from distutils.version import LooseVersion

# All PonyORM versions between 0.5.3 and 0.6.2 have a bug with PyMySQL
# see https://github.com/ponyorm/pony/issues/87#issuecomment-88564346
if os.environ.get('DB') == 'mysql' and LooseVersion('0.5.3') < LooseVersion(__version__) < LooseVersion('0.6.2'):
    del sys.modules['MySQLdb']
    del sys.modules['_mysql']

from .models.pony import *


class BasePonyPartitionTestCase(object):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.pony']
        with capture() as (out, _):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ.get('DB') == 'sqlite', 'Not a SQLite build')
class SQLitePonyPartitionTestCase(BasePonyPartitionTestCase, unittest.TestCase):
    def test_dummy(self):
        with db_session:
            object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateDay.get_by_sql(
                'SELECT * FROM test_rangedateday WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ.get('DB') in ('pgsql', 'postgresql'), 'Not a PostgreSQL build')
class PostgresqlPonyPartitionTestCase(BasePonyPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        with db_session:
            object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateDay.get_by_sql('SELECT * FROM test_rangedateday_y2014d105 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        with db_session:
            object1 = RangeDateDay(name='foo')
            commit()
            object2 = RangeDateDay.get_by_sql('SELECT * FROM test_rangedateday_null WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        with db_session:
            object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateWeek.get_by_sql('SELECT * FROM test_rangedateweek_y2014w16 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        with db_session:
            object1 = RangeDateWeek(name='foo')
            commit()
            object2 = RangeDateWeek.get_by_sql('SELECT * FROM test_rangedateweek_null WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        with db_session:
            object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateMonth.get_by_sql('SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        with db_session:
            object1 = RangeDateMonth(name='foo')
            commit()
            object2 = RangeDateMonth.get_by_sql('SELECT * FROM test_rangedatemonth_null WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        with db_session:
            object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateYear.get_by_sql('SELECT * FROM test_rangedateyear_y2014 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        with db_session:
            object1 = RangeDateYear(name='foo')
            commit()
            object2 = RangeDateYear.get_by_sql('SELECT * FROM test_rangedateyear_null WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        with db_session:
            object1 = RangeInteger2(name='foo', num=3)
            object3 = RangeInteger5(name='foo', num=3)
            commit()
            object2 = RangeInteger2.get_by_sql('SELECT * FROM test_rangeinteger2_3_4 WHERE id = $object1.id')
            object4 = RangeInteger5.get_by_sql('SELECT * FROM test_rangeinteger5_1_5 WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        with db_session:
            object1 = RangeInteger2(name='foo', num=0)
            object3 = RangeInteger5(name='foo', num=0)
            commit()
            object2 = RangeInteger2.get_by_sql('SELECT * FROM test_rangeinteger2_0 WHERE id = $object1.id')
            object4 = RangeInteger5.get_by_sql('SELECT * FROM test_rangeinteger5_0 WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        with db_session:
            object1 = RangeInteger2(name='foo', num=-3)
            object3 = RangeInteger5(name='foo', num=-3)
            commit()
            object2 = RangeInteger2.get_by_sql('SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = $object1.id')
            object4 = RangeInteger5.get_by_sql('SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        with db_session:
            object1 = RangeInteger2(name='foo')
            object3 = RangeInteger5(name='foo')
            commit()
            object2 = RangeInteger2.get_by_sql('SELECT * FROM test_rangeinteger2_null WHERE id = $object1.id')
            object4 = RangeInteger5.get_by_sql('SELECT * FROM test_rangeinteger5_null WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        with db_session:
            object1 = RangeStringFirstchars2(name='foo', title='abcdef')
            object3 = RangeStringFirstchars5(name='foo', title='abcdef')
            commit()
            object2 = RangeStringFirstchars2.get_by_sql(
                'SELECT * FROM test_rangestring_firstchars2_ab WHERE id = $object1.id')
            object4 = RangeStringFirstchars5.get_by_sql(
                'SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        with db_session:
            object1 = RangeStringFirstchars2(name='foo', title=';<abcdef')
            object3 = RangeStringFirstchars5(name='foo', title='ab;<cdef')
            commit()
            object2 = RangeStringFirstchars2.get_by_sql(
                'SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = $object1.id')
            object4 = RangeStringFirstchars5.get_by_sql(
                'SELECT * FROM "test_rangestring_firstchars5_ab;<c" WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        with db_session:
            object1 = RangeStringFirstchars2(name='foo')
            object3 = RangeStringFirstchars5(name='foo')
            commit()
            object2 = RangeStringFirstchars2.get_by_sql(
                'SELECT * FROM test_rangestring_firstchars2_null WHERE id = $object1.id')
            object4 = RangeStringFirstchars5.get_by_sql(
                'SELECT * FROM test_rangestring_firstchars5_null WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        with db_session:
            object1 = RangeStringLastchars2(name='foo', title='abcdef')
            object3 = RangeStringLastchars5(name='foo', title='abcdef')
            commit()
            object2 = RangeStringLastchars2.get_by_sql(
                'SELECT * FROM test_rangestring_lastchars2_ef WHERE id = $object1.id')
            object4 = RangeStringLastchars5.get_by_sql(
                'SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        with db_session:
            object1 = RangeStringLastchars2(name='foo', title='abcd;<')
            object3 = RangeStringLastchars5(name='foo', title='abcd;<')
            commit()
            object2 = RangeStringLastchars2.get_by_sql(
                'SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = $object1.id')
            object4 = RangeStringLastchars5.get_by_sql(
                'SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        with db_session:
            object1 = RangeStringLastchars2(name='foo')
            object3 = RangeStringLastchars5(name='foo')
            commit()
            object2 = RangeStringLastchars2.get_by_sql(
                'SELECT * FROM test_rangestring_lastchars2_null WHERE id = $object1.id')
            object4 = RangeStringLastchars5.get_by_sql(
                'SELECT * FROM test_rangestring_lastchars5_null WHERE id = $object3.id')

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


@unittest.skipUnless(os.environ.get('DB') == 'mysql', 'Not a MySQL build')
class MysqlPonyPartitionTestCase(BasePonyPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        with db_session:
            object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateDay.get_by_sql(
                'SELECT * FROM test_rangedateday WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        with db_session:
            object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateWeek.get_by_sql(
                'SELECT * FROM test_rangedateweek WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        with db_session:
            object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateMonth.get_by_sql(
                'SELECT * FROM test_rangedatemonth WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        with db_session:
            object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateYear.get_by_sql(
                'SELECT * FROM test_rangedateyear WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)
