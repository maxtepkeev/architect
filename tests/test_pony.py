import os
import sys

from . import unittest, capture

if not os.environ.get('PONY'):
    raise unittest.SkipTest('Not a Pony build')

from pony import __version__
from distutils.version import LooseVersion

# All PonyORM versions between 0.5.3 and 0.6.2 have a bug with PyMySQL
# see https://github.com/ponyorm/pony/issues/87#issuecomment-88564346
if LooseVersion('0.5.3') < LooseVersion(__version__) < LooseVersion('0.6.2'):
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


@unittest.skipUnless(os.environ.get('DB') == 'postgresql', 'Not a PostgreSQL build')
class PostgresqlPonyPartitionTestCase(BasePonyPartitionTestCase, unittest.TestCase):
    def test_range_date_day(self):
        with db_session:
            object1 = RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateDay.get_by_sql('SELECT * FROM test_rangedateday_y2014d105 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_week(self):
        with db_session:
            object1 = RangeDateWeek(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateWeek.get_by_sql('SELECT * FROM test_rangedateweek_y2014w16 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_month(self):
        with db_session:
            object1 = RangeDateMonth(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateMonth.get_by_sql('SELECT * FROM test_rangedatemonth_y2014m04 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)

    def test_range_date_year(self):
        with db_session:
            object1 = RangeDateYear(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))
            commit()
            object2 = RangeDateYear.get_by_sql('SELECT * FROM test_rangedateyear_y2014 WHERE id = $object1.id')

        self.assertTrue(object1.name, object2.name)


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
