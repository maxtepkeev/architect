import os
import sys
import datetime

from tests import unittest, capture

if not os.environ.get('PONY'):
    raise unittest.SkipTest('Not a Pony build')

from tests.models.pony import *


class PonyPartitionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        sys.argv = ['architect', 'partition', '--module', 'tests.models.pony']
        with capture() as (out, _):
            search = 'successfully (re)configured the database for the following models'
            assert search in out, '{0} not in {1}'.format(search, out)

    def test_raises_partition_column_error(self):
        RangeDateDay.PartitionableMeta.partition_column = 'foo'

        with self.assertRaises(CommitException):
            with db_session:
                RangeDateDay(name='foo', created=datetime.datetime(2014, 4, 15, 18, 44, 23))

        RangeDateDay.PartitionableMeta.partition_column = 'created'

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
