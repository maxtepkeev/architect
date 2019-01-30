"""
Tests Django specific behaviour.
"""

import os
import datetime

from . import unittest, capture

if not os.environ.get('DJANGO') or not os.environ.get('DB'):
    raise unittest.SkipTest('Not a Django build')

from .models.django import *


def setUpModule():
    sys.argv = ['architect', 'partition', '--module', 'tests.models.django']
    with capture() as (out, _):
        search = 'successfully (re)configured the database for the following models'
        assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ['DB'] in ('sqlite', 'all'), 'Not a SQLite build')
class SQLiteDjangoPartitionTestCase(unittest.TestCase):
    def test_raises_option_not_set_error(self):
        from architect.exceptions import OptionNotSetError
        del SqliteRangeDateDay.architect.partition.options['column']

        with self.assertRaises(OptionNotSetError):
            SqliteRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        SqliteRangeDateDay.architect.partition.options['column'] = 'created'

    def test_raises_partition_column_error(self):
        from architect.exceptions import PartitionColumnError
        SqliteRangeDateDay.architect.partition.options['column'] = 'foo'

        with self.assertRaises(PartitionColumnError):
            SqliteRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        SqliteRangeDateDay.architect.partition.options['column'] = 'created'

    def test_dummy(self):
        object1 = SqliteRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = SqliteRangeDateDay.objects.raw('SELECT * FROM test_rangedateday WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ['DB'] in ('pgsql', 'all'), 'Not a PostgreSQL build')
class PostgresqlDjangoPartitionTestCase(unittest.TestCase):
    def test_raises_option_not_set_error(self):
        from architect.exceptions import OptionNotSetError
        del PgsqlRangeDateDay.architect.partition.options['column']

        with self.assertRaises(OptionNotSetError):
            PgsqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        PgsqlRangeDateDay.architect.partition.options['column'] = 'created'

    def test_raises_partition_column_error(self):
        from architect.exceptions import PartitionColumnError
        PgsqlRangeDateDay.architect.partition.options['column'] = 'foo'

        with self.assertRaises(PartitionColumnError):
            PgsqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        PgsqlRangeDateDay.architect.partition.options['column'] = 'created'

    def test_range_date_day(self):
        object1 = PgsqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateDay.objects.raw(
            'SELECT * FROM test_rangedateday_y2014d105 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        object1 = PgsqlRangeDateDay.objects.create(name='foo')
        object2 = PgsqlRangeDateDay.objects.raw('SELECT * FROM test_rangedateday_null WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_return_null(self):
        object1 = PgsqlRangeDateDayReturnNULL.objects.create(id=1, name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateDayReturnNULL.objects.raw(
            'SELECT * FROM test_rangedateday_return_null_y2014d105 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = PgsqlRangeDateWeek.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateWeek.objects.raw(
            'SELECT * FROM test_rangedateweek_y2014w16 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        object1 = PgsqlRangeDateWeek.objects.create(name='foo')
        object2 = PgsqlRangeDateWeek.objects.raw(
            'SELECT * FROM test_rangedateweek_null WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_return_null(self):
        object1 = PgsqlRangeDateWeekReturnNULL.objects.create(id=1, name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateWeekReturnNULL.objects.raw(
            'SELECT * FROM test_rangedateweek_return_null_y2014w16 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = PgsqlRangeDateMonth.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateMonth.objects.raw(
            'SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        object1 = PgsqlRangeDateMonth.objects.create(name='foo')
        object2 = PgsqlRangeDateMonth.objects.raw(
            'SELECT * FROM test_rangedatemonth_null WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_return_null(self):
        object1 = PgsqlRangeDateMonthReturnNULL.objects.create(id=1, name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateMonthReturnNULL.objects.raw(
            'SELECT * FROM test_rangedatemonth_return_null_y2014m04 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = PgsqlRangeDateYear.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateYear.objects.raw(
            'SELECT * FROM test_rangedateyear_y2014 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        object1 = PgsqlRangeDateYear.objects.create(name='foo')
        object2 = PgsqlRangeDateYear.objects.raw(
            'SELECT * FROM test_rangedateyear_null WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_return_null(self):
        object1 = PgsqlRangeDateYearReturnNULL.objects.create(id=1, name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = PgsqlRangeDateYearReturnNULL.objects.raw(
            'SELECT * FROM test_rangedateyear_return_null_y2014 WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        object1 = PgsqlRangeInteger2.objects.create(name='foo', num=3)
        object2 = PgsqlRangeInteger2.objects.raw('SELECT * FROM test_rangeinteger2_3_4 WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeInteger5.objects.create(name='foo', num=3)
        object4 = PgsqlRangeInteger5.objects.raw('SELECT * FROM test_rangeinteger5_1_5 WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        object1 = PgsqlRangeInteger2.objects.create(name='foo', num=0)
        object2 = PgsqlRangeInteger2.objects.raw('SELECT * FROM test_rangeinteger2_0 WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeInteger5.objects.create(name='foo', num=0)
        object4 = PgsqlRangeInteger5.objects.raw('SELECT * FROM test_rangeinteger5_0 WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        object1 = PgsqlRangeInteger2.objects.create(name='foo', num=-3)
        object2 = PgsqlRangeInteger2.objects.raw(
            'SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeInteger5.objects.create(name='foo', num=-3)
        object4 = PgsqlRangeInteger5.objects.raw(
            'SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        object1 = PgsqlRangeInteger2.objects.create(name='foo')
        object2 = PgsqlRangeInteger2.objects.raw('SELECT * FROM test_rangeinteger2_null WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeInteger5.objects.create(name='foo')
        object4 = PgsqlRangeInteger5.objects.raw('SELECT * FROM test_rangeinteger5_null WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_positive_return_null(self):
        object1 = PgsqlRangeInteger2ReturnNULL.objects.create(id=1, name='foo', num=3)
        object2 = PgsqlRangeInteger2ReturnNULL.objects.raw('SELECT * FROM test_rangeinteger2_return_null_3_4 WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeInteger5ReturnNULL.objects.create(id=1, name='foo', num=3)
        object4 = PgsqlRangeInteger5ReturnNULL.objects.raw('SELECT * FROM test_rangeinteger5_return_null_1_5 WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        object1 = PgsqlRangeStringFirstchars2.objects.create(name='foo', title='abcdef')
        object2 = PgsqlRangeStringFirstchars2.objects.raw(
            'SELECT * FROM test_rangestring_firstchars2_ab WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringFirstchars5.objects.create(name='foo', title='abcdef')
        object4 = PgsqlRangeStringFirstchars5.objects.raw(
            'SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        object1 = PgsqlRangeStringFirstchars2.objects.create(name='foo', title=';<abcdef')
        object2 = PgsqlRangeStringFirstchars2.objects.raw(
            'SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringFirstchars5.objects.create(name='foo', title='ab;<cdef')
        object4 = PgsqlRangeStringFirstchars5.objects.raw(
            'SELECT * FROM "test_rangestring_firstchars5_ab;<c" WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        object1 = PgsqlRangeStringFirstchars2.objects.create(name='foo')
        object2 = PgsqlRangeStringFirstchars2.objects.raw(
            'SELECT * FROM test_rangestring_firstchars2_null WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringFirstchars5.objects.create(name='foo')
        object4 = PgsqlRangeStringFirstchars5.objects.raw(
            'SELECT * FROM test_rangestring_firstchars5_null WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_return_null(self):
        object1 = PgsqlRangeStringFirstchars2ReturnNULL.objects.create(id=1, name='foo', title='abcdef')
        object2 = PgsqlRangeStringFirstchars2ReturnNULL.objects.raw(
            'SELECT * FROM test_rangestring_firstchars2_return_null_ab WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringFirstchars5ReturnNULL.objects.create(id=1, name='foo', title='abcdef')
        object4 = PgsqlRangeStringFirstchars5ReturnNULL.objects.raw(
            'SELECT * FROM test_rangestring_firstchars5_return_null_abcde WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        object1 = PgsqlRangeStringLastchars2.objects.create(name='foo', title='abcdef')
        object2 = PgsqlRangeStringLastchars2.objects.raw(
            'SELECT * FROM test_rangestring_lastchars2_ef WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringLastchars5.objects.create(name='foo', title='abcdef')
        object4 = PgsqlRangeStringLastchars5.objects.raw(
            'SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        object1 = PgsqlRangeStringLastchars2.objects.create(name='foo', title='abcd;<')
        object2 = PgsqlRangeStringLastchars2.objects.raw(
            'SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringLastchars5.objects.create(name='foo', title='abcd;<')
        object4 = PgsqlRangeStringLastchars5.objects.raw(
            'SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        object1 = PgsqlRangeStringLastchars2.objects.create(name='foo')
        object2 = PgsqlRangeStringLastchars2.objects.raw(
            'SELECT * FROM test_rangestring_lastchars2_null WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringLastchars5.objects.create(name='foo')
        object4 = PgsqlRangeStringLastchars5.objects.raw(
            'SELECT * FROM test_rangestring_lastchars5_null WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_return_null(self):
        object1 = PgsqlRangeStringLastchars2ReturnNULL.objects.create(id=1, name='foo', title='abcdef')
        object2 = PgsqlRangeStringLastchars2ReturnNULL.objects.raw(
            'SELECT * FROM test_rangestring_lastchars2_return_null_ef WHERE id = %s', [object1.id])[0]
        object3 = PgsqlRangeStringLastchars5ReturnNULL.objects.create(id=1, name='foo', title='abcdef')
        object4 = PgsqlRangeStringLastchars5ReturnNULL.objects.raw(
            'SELECT * FROM test_rangestring_lastchars5_return_null_bcdef WHERE id = %s', [object3.id])[0]

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


@unittest.skipUnless(os.environ['DB'] in ('mysql', 'all'), 'Not a MySQL build')
class MysqlDjangoPartitionTestCase(unittest.TestCase):
    def test_raises_option_not_set_error(self):
        from architect.exceptions import OptionNotSetError
        del MysqlRangeDateDay.architect.partition.options['column']

        with self.assertRaises(OptionNotSetError):
            MysqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        MysqlRangeDateDay.architect.partition.options['column'] = 'created'

    def test_raises_partition_column_error(self):
        from architect.exceptions import PartitionColumnError
        MysqlRangeDateDay.architect.partition.options['column'] = 'foo'

        with self.assertRaises(PartitionColumnError):
            MysqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        MysqlRangeDateDay.architect.partition.options['column'] = 'created'

    def test_range_date_day(self):
        object1 = MysqlRangeDateDay.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateDay.objects.raw('SELECT * FROM test_rangedateday WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = MysqlRangeDateWeek.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateWeek.objects.raw('SELECT * FROM test_rangedateweek WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = MysqlRangeDateMonth.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateMonth.objects.raw('SELECT * FROM test_rangedatemonth WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = MysqlRangeDateYear.objects.create(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        object2 = MysqlRangeDateYear.objects.raw('SELECT * FROM test_rangedateyear WHERE id = %s', [object1.id])[0]

        self.assertTrue(object1.name, object2.name)
