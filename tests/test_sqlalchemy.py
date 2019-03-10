"""
Tests SQLAlchemy specific behaviour.
"""

import os
import sys
import datetime

from . import unittest, capture

if not os.environ.get('SQLALCHEMY') or not os.environ.get('DB'):
    raise unittest.SkipTest('Not a SQLAlchemy build')

from .models.sqlalchemy import *
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


def setUpModule():
    sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlalchemy']
    with capture() as (out, _):
        search = 'successfully (re)configured the database for the following models'
        assert search in out, '{0} not in {1}'.format(search, out)


@unittest.skipUnless(os.environ['DB'] in ('sqlite', 'all'), 'Not a SQLite build')
class SQLiteSqlAlchemyPartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = sessionmaker(bind=sqlite_engine)()

    def test_bound_metadata(self):
        url = SqliteRangeDateDay.architect.partition.options.pop('db')
        SqliteRangeDateDay.metadata.bind = sqlite_engine
        self.session.add(SqliteRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
        self.session.commit()
        self.session.rollback()
        SqliteRangeDateDay.metadata.bind = None
        SqliteRangeDateDay.architect.partition.options['db'] = url

    def test_raises_db_not_provided_error(self):
        from architect.exceptions import OptionNotSetError

        url = SqliteRangeDateDay.architect.partition.options.pop('db')

        with self.assertRaises(OptionNotSetError):
            self.session.add(SqliteRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        SqliteRangeDateDay.architect.partition.options['db'] = url

    def test_raises_option_value_error(self):
        from architect.exceptions import OptionValueError

        url = SqliteRangeDateDay.architect.partition.options['db']
        SqliteRangeDateDay.architect.partition.options['db'] = 'foo'

        with self.assertRaises(OptionValueError):
            self.session.add(SqliteRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        SqliteRangeDateDay.architect.partition.options['db'] = url

    def test_dummy(self):
        object1 = SqliteRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(SqliteRangeDateDay).from_statement(
            text('SELECT * FROM TEST_rangedateday WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)


@unittest.skipUnless(os.environ['DB'] in ('pgsql', 'all'), 'Not a PostgreSQL build')
class PostgresqlSqlAlchemyPartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = sessionmaker(bind=pgsql_engine)()

    def test_bound_metadata(self):
        url = PgsqlRangeDateDay.architect.partition.options.pop('db')
        PgsqlRangeDateDay.metadata.bind = pgsql_engine
        self.session.add(PgsqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
        self.session.commit()
        self.session.rollback()
        PgsqlRangeDateDay.metadata.bind = None
        PgsqlRangeDateDay.architect.partition.options['db'] = url

    def test_raises_db_not_provided_error(self):
        from architect.exceptions import OptionNotSetError

        url = PgsqlRangeDateDay.architect.partition.options.pop('db')

        with self.assertRaises(OptionNotSetError):
            self.session.add(PgsqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        PgsqlRangeDateDay.architect.partition.options['db'] = url

    def test_raises_option_value_error(self):
        from architect.exceptions import OptionValueError

        url = PgsqlRangeDateDay.architect.partition.options['db']
        PgsqlRangeDateDay.architect.partition.options['db'] = 'foo'

        with self.assertRaises(OptionValueError):
            self.session.add(PgsqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        PgsqlRangeDateDay.architect.partition.options['db'] = url

    def test_range_date_day(self):
        object1 = PgsqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateDay).from_statement(
            text('SELECT * FROM TEST_rangedateday_y2014d105 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_day_null(self):
        object1 = PgsqlRangeDateDay(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateDay).from_statement(
            text('SELECT * FROM TEST_rangedateday_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = PgsqlRangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateWeek).from_statement(
            text('SELECT * FROM TEST_rangedateweek_y2014w16 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week_null(self):
        object1 = PgsqlRangeDateWeek(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateWeek).from_statement(
            text('SELECT * FROM TEST_rangedateweek_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = PgsqlRangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateMonth).from_statement(
            text('SELECT * FROM TEST_rangedatemonth_y2014m04 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month_null(self):
        object1 = PgsqlRangeDateMonth(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateMonth).from_statement(
            text('SELECT * FROM TEST_rangedatemonth_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = PgsqlRangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateYear).from_statement(
            text('SELECT * FROM TEST_rangedateyear_y2014 WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year_null(self):
        object1 = PgsqlRangeDateYear(name='foo')
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(PgsqlRangeDateYear).from_statement(
            text('SELECT * FROM TEST_rangedateyear_null WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_integer_positive(self):
        object1 = PgsqlRangeInteger2(name='foo', num=3)
        object3 = PgsqlRangeInteger5(name='foo', num=3)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeInteger2).from_statement(
            text('SELECT * FROM TEST_rangeinteger2_3_4 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeInteger5).from_statement(
            text('SELECT * FROM TEST_rangeinteger5_1_5 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_zero(self):
        object1 = PgsqlRangeInteger2(name='foo', num=0)
        object3 = PgsqlRangeInteger5(name='foo', num=0)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeInteger2).from_statement(
            text('SELECT * FROM TEST_rangeinteger2_0 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeInteger5).from_statement(
            text('SELECT * FROM TEST_rangeinteger5_0 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_negative(self):
        object1 = PgsqlRangeInteger2(name='foo', num=-3)
        object3 = PgsqlRangeInteger5(name='foo', num=-3)
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeInteger2).from_statement(
            text('SELECT * FROM TEST_rangeinteger2_m4_m3 WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeInteger5).from_statement(
            text('SELECT * FROM TEST_rangeinteger5_m5_m1 WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_integer_null(self):
        object1 = PgsqlRangeInteger2(name='foo')
        object3 = PgsqlRangeInteger5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeInteger2).from_statement(
            text('SELECT * FROM TEST_rangeinteger2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeInteger5).from_statement(
            text('SELECT * FROM TEST_rangeinteger5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo', title='abcdef')
        object3 = PgsqlRangeStringFirstchars5(name='foo', title='abcdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringFirstchars2).from_statement(
            text('SELECT * FROM "TEST_rangestring_firstchars2_ab" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringFirstchars5).from_statement(
            text('SELECT * FROM "TEST_rangestring_firstchars5_abcde" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_special_characters(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo', title=';<abcdef')
        object3 = PgsqlRangeStringFirstchars5(name='foo', title='ab;<cdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringFirstchars2).from_statement(
            text('SELECT * FROM "TEST_rangestring_firstchars2_;<" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringFirstchars5).from_statement(
            text('SELECT * FROM "TEST_rangestring_firstchars5_ab;<c" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_firstchars_null(self):
        object1 = PgsqlRangeStringFirstchars2(name='foo')
        object3 = PgsqlRangeStringFirstchars5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringFirstchars2).from_statement(
            text('SELECT * FROM TEST_rangestring_firstchars2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringFirstchars5).from_statement(
            text('SELECT * FROM TEST_rangestring_firstchars5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars(self):
        object1 = PgsqlRangeStringLastchars2(name='foo', title='abcdef')
        object3 = PgsqlRangeStringLastchars5(name='foo', title='abcdef')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringLastchars2).from_statement(
            text('SELECT * FROM "TEST_rangestring_lastchars2_ef" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringLastchars5).from_statement(
            text('SELECT * FROM "TEST_rangestring_lastchars5_bcdef" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_special_characters(self):
        object1 = PgsqlRangeStringLastchars2(name='foo', title='abcd;<')
        object3 = PgsqlRangeStringLastchars5(name='foo', title='abcd;<')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringLastchars2).from_statement(
            text('SELECT * FROM "TEST_rangestring_lastchars2_;<" WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringLastchars5).from_statement(
            text('SELECT * FROM "TEST_rangestring_lastchars5_bcd;<" WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)

    def test_range_string_lastchars_null(self):
        object1 = PgsqlRangeStringLastchars2(name='foo')
        object3 = PgsqlRangeStringLastchars5(name='foo')
        self.session.add_all([object1, object3])
        self.session.commit()

        object2 = self.session.query(PgsqlRangeStringLastchars2).from_statement(
            text('SELECT * FROM TEST_rangestring_lastchars2_null WHERE id = :id')
        ).params(id=object1.id).first()
        object4 = self.session.query(PgsqlRangeStringLastchars5).from_statement(
            text('SELECT * FROM TEST_rangestring_lastchars5_null WHERE id = :id')
        ).params(id=object3.id).first()

        self.assertTrue(object1.name, object2.name)
        self.assertTrue(object3.name, object4.name)


@unittest.skipUnless(os.environ['DB'] in ('mysql', 'all'), 'Not a MySQL build')
class MysqlSqlAlchemyPartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.session = sessionmaker(bind=mysql_engine)()

    def test_bound_metadata(self):
        url = MysqlRangeDateDay.architect.partition.options.pop('db')
        MysqlRangeDateDay.metadata.bind = mysql_engine
        self.session.add(MysqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
        self.session.commit()
        self.session.rollback()
        MysqlRangeDateDay.metadata.bind = None
        MysqlRangeDateDay.architect.partition.options['db'] = url

    def test_raises_db_not_provided_error(self):
        from architect.exceptions import OptionNotSetError

        url = MysqlRangeDateDay.architect.partition.options.pop('db')

        with self.assertRaises(OptionNotSetError):
            self.session.add(MysqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        MysqlRangeDateDay.architect.partition.options['db'] = url

    def test_raises_option_value_error(self):
        from architect.exceptions import OptionValueError

        url = MysqlRangeDateDay.architect.partition.options['db']
        MysqlRangeDateDay.architect.partition.options['db'] = 'foo'

        with self.assertRaises(OptionValueError):
            self.session.add(MysqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        MysqlRangeDateDay.architect.partition.options['db'] = url

    def test_range_date_day(self):
        object1 = MysqlRangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(MysqlRangeDateDay).from_statement(
            text('SELECT * FROM TEST_rangedateday WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = MysqlRangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(MysqlRangeDateWeek).from_statement(
            text('SELECT * FROM TEST_rangedateweek WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = MysqlRangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(MysqlRangeDateMonth).from_statement(
            text('SELECT * FROM TEST_rangedatemonth WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = MysqlRangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(MysqlRangeDateYear).from_statement(
            text('SELECT * FROM TEST_rangedateyear WHERE id = :id')
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)
