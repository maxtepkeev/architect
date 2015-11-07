"""
Tests SQLAlchemy specific behaviour.
"""

import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('SQLALCHEMY'):
    raise unittest.SkipTest('Not a SQLAlchemy build')

from .models.sqlalchemy import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


class BaseSqlAlchemyPartitionTestCase(object):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlalchemy']
        with capture() as (out, _):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)
        cls.session = sessionmaker(bind=engine)()

    def test_bound_metadata(self):
        url = RangeDateDay.architect.partition.options.pop('db')
        RangeDateDay.metadata.bind = engine
        self.session.add(RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
        self.session.commit()
        self.session.rollback()
        RangeDateDay.metadata.bind = None
        RangeDateDay.architect.partition.options['db'] = url

    def test_raises_db_not_provided_error(self):
        from architect.exceptions import OptionNotSetError
        url = RangeDateDay.architect.partition.options.pop('db')

        with self.assertRaises(OptionNotSetError):
            self.session.add(RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        RangeDateDay.architect.partition.options['db'] = url

    def test_raises_option_value_error(self):
        from architect.exceptions import OptionValueError

        url = RangeDateDay.architect.partition.options['db']
        RangeDateDay.architect.partition.options['db'] = 'foo'

        with self.assertRaises(OptionValueError):
            self.session.add(RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        RangeDateDay.architect.partition.options['db'] = url


@unittest.skipUnless(os.environ.get('DB') == 'sqlite', 'Not a SQLite build')
class SQLiteSqlAlchemyPartitionTestCase(BaseSqlAlchemyPartitionTestCase, unittest.TestCase):
    def test_dummy(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateDay).from_statement(
            text('SELECT * FROM test_rangedateday WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ.get('DB') in ('pgsql', 'postgresql'), 'Not a PostgreSQL build')
class PostgresqlSqlAlchemyPartitionTestCase(BaseSqlAlchemyPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateDay).from_statement(
            text('SELECT * FROM test_rangedateday_y2014d105 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        object1 = RangeDateDay(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateDay).from_statement(
            text('SELECT * FROM test_rangedateday_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateWeek).from_statement(
            text('SELECT * FROM test_rangedateweek_y2014w16 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        object1 = RangeDateWeek(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateWeek).from_statement(
            text('SELECT * FROM test_rangedateweek_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateMonth).from_statement(
            text('SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        object1 = RangeDateMonth(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateMonth).from_statement(
            text('SELECT * FROM test_rangedatemonth_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateYear).from_statement(
            text('SELECT * FROM test_rangedateyear_y2014 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        object1 = RangeDateYear(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateYear).from_statement(
            text('SELECT * FROM test_rangedateyear_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        object1 = RangeInteger2(name='foo', num=3)
        object3 = RangeInteger5(name='foo', num=3)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeInteger2).from_statement(
            text('SELECT * FROM test_rangeinteger2_3_4 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeInteger5).from_statement(
            text('SELECT * FROM test_rangeinteger5_1_5 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        object1 = RangeInteger2(name='foo', num=0)
        object3 = RangeInteger5(name='foo', num=0)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeInteger2).from_statement(
            text('SELECT * FROM test_rangeinteger2_0 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeInteger5).from_statement(
            text('SELECT * FROM test_rangeinteger5_0 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        object1 = RangeInteger2(name='foo', num=-3)
        object3 = RangeInteger5(name='foo', num=-3)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeInteger2).from_statement(
            text('SELECT * FROM test_rangeinteger2_m4_m3 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeInteger5).from_statement(
            text('SELECT * FROM test_rangeinteger5_m5_m1 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        object1 = RangeInteger2(name='foo')
        object3 = RangeInteger5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeInteger2).from_statement(
            text('SELECT * FROM test_rangeinteger2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeInteger5).from_statement(
            text('SELECT * FROM test_rangeinteger5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        object1 = RangeStringFirstchars2(name='foo', title='abcdef')
        object3 = RangeStringFirstchars5(name='foo', title='abcdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringFirstchars2).from_statement(
            text('SELECT * FROM test_rangestring_firstchars2_ab WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringFirstchars5).from_statement(
            text('SELECT * FROM test_rangestring_firstchars5_abcde WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        object1 = RangeStringFirstchars2(name='foo', title=';<abcdef')
        object3 = RangeStringFirstchars5(name='foo', title='ab;<cdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringFirstchars2).from_statement(
            text('SELECT * FROM "test_rangestring_firstchars2_;<" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringFirstchars5).from_statement(
            text('SELECT * FROM "test_rangestring_firstchars5_ab;<c" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        object1 = RangeStringFirstchars2(name='foo')
        object3 = RangeStringFirstchars5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringFirstchars2).from_statement(
            text('SELECT * FROM test_rangestring_firstchars2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringFirstchars5).from_statement(
            text('SELECT * FROM test_rangestring_firstchars5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        object1 = RangeStringLastchars2(name='foo', title='abcdef')
        object3 = RangeStringLastchars5(name='foo', title='abcdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringLastchars2).from_statement(
            text('SELECT * FROM test_rangestring_lastchars2_ef WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringLastchars5).from_statement(
            text('SELECT * FROM test_rangestring_lastchars5_bcdef WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        object1 = RangeStringLastchars2(name='foo', title='abcd;<')
        object3 = RangeStringLastchars5(name='foo', title='abcd;<')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringLastchars2).from_statement(
            text('SELECT * FROM "test_rangestring_lastchars2_;<" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringLastchars5).from_statement(
            text('SELECT * FROM "test_rangestring_lastchars5_bcd;<" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        object1 = RangeStringLastchars2(name='foo')
        object3 = RangeStringLastchars5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(RangeStringLastchars2).from_statement(
            text('SELECT * FROM test_rangestring_lastchars2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(RangeStringLastchars5).from_statement(
            text('SELECT * FROM test_rangestring_lastchars5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


@unittest.skipUnless(os.environ.get('DB') == 'mysql', 'Not a MySQL build')
class MysqlSqlAlchemyPartitionTestCase(BaseSqlAlchemyPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateDay).from_statement(
            text('SELECT * FROM test_rangedateday WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateWeek).from_statement(
            text('SELECT * FROM test_rangedateweek WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateMonth).from_statement(
            text('SELECT * FROM test_rangedatemonth WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateYear).from_statement(
            text('SELECT * FROM test_rangedateyear WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)
