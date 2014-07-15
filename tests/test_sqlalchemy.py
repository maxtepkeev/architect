import os
import sys
import datetime

from tests import unittest, capture

if not os.environ.get('SQLALCHEMY'):
    raise unittest.SkipTest('Not a SQLAlchemy build')

from tests.models.sqlalchemy import *
from sqlalchemy.orm import sessionmaker


class SqlAlchemyPartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlalchemy', '--connection', dsn]
        with capture() as (out, err):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)
        cls.session = sessionmaker(bind=engine)()

    def test_dsn_not_provided_error(self):
        from architect.exceptions import DsnNotProvidedError
        sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlalchemy']
        with capture() as (_, err):
            self.assertIn(str(DsnNotProvidedError()).lower(), err.lower())

    def test_bad_dsn_provided_error(self):
        from architect.exceptions import DsnParseError
        sys.argv = ['architect', 'partition', '--module', 'tests.models.sqlalchemy', '--connection', 'foobar']
        with capture() as (_, err):
            self.assertIn(str(DsnParseError(current='foobar')).lower(), err.lower())

    def test_raises_partition_column_error(self):
        from architect.exceptions import PartitionColumnError
        RangeDateDay.PartitionableMeta.partition_column = 'foo'

        with self.assertRaises(PartitionColumnError):
            self.session.add(RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23)))
            self.session.commit()

        self.session.rollback()
        RangeDateDay.PartitionableMeta.partition_column = 'created'

    def test_range_date_day(self):
        object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateDay).from_statement(
            'SELECT * FROM test_rangedateday_y2014d105 WHERE id =:id'
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateWeek).from_statement(
            'SELECT * FROM test_rangedateweek_y2014w16 WHERE id =:id'
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateMonth).from_statement(
            'SELECT * FROM test_rangedatemonth_y2014m04 WHERE id =:id'
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
        self.session.add(object1)
        self.session.commit()

        object2 = self.session.query(RangeDateYear).from_statement(
            'SELECT * FROM test_rangedateyear_y2014 WHERE id =:id'
        ).params(id=object1.id).first()

        self.assertTrue(object1.name, object2.name)
