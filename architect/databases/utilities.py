"""
Defines database related utilities.
"""

import os
import pkgutil
import datetime

from ..exceptions import DatabaseError


def get_database(dialect):
    """
    Returns requested database package with modules that provide additional functionality.

    :param string dialect: (required). Database dialect name.
    """
    aliases = {
        ('mysql',): 'mysql',
        ('sqlite',): 'sqlite',
        ('pgsql', 'postgres', 'postgresql'): 'postgresql',
    }

    dialect = next((aliases[alias] for alias in aliases if dialect in alias), dialect)
    names = [str(mod[1]) for mod in pkgutil.iter_modules([os.path.join(os.path.dirname(__file__), dialect)])]

    try:
        return __import__('{0}'.format(dialect), globals(), level=1, fromlist=names)
    except ImportError:
        raise DatabaseError(
            current=dialect,
            allowed=[name for _, name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]) if is_pkg])


class DateTime(object):
    """
    Provides date and time calculations for some database backends.
    """
    def __init__(self, now, template='%Y-%m-%d %H:%M:%S'):
        """
        :param object now: (required). Date/Datetime object to work with.
        :param string template: (optional). Format of datetime string representation.
        """
        self.now = datetime.datetime(now.year, now.month, now.day) if type(now) is datetime.date else now
        self.template = template

    def get_period(self, period):
        """
        Dynamically returns beginning and an end depending on the given period.

        :param string period: (required). Name of the period.
        """
        return getattr(self, '_get_{0}_period'.format(period))()

    def _get_day_period(self):
        """
        Returns beginning and an end for a day period.
        """
        start = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = self.now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return start.strftime(self.template), end.strftime(self.template)

    def _get_week_period(self):
        """
        Returns beginning and an end for a week period.
        """
        dt = datetime.datetime(self.now.year, 1, 1)

        if dt.weekday() > 3:
            dt += datetime.timedelta(7 - dt.weekday())
        else:
            dt -= datetime.timedelta(dt.weekday())

        days = datetime.timedelta((int(self.now.strftime('%V')) - 1) * 7)

        start = (dt + days)
        end = (dt + days + datetime.timedelta(6)).replace(hour=23, minute=59, second=59, microsecond=999999)

        return start.strftime(self.template), end.strftime(self.template)

    def _get_month_period(self):
        """
        Returns beginning and an end for a month period.
        """
        start = datetime.datetime(self.now.year, self.now.month, 1)

        if self.now.month == 12:
            end = datetime.datetime(self.now.year, self.now.month, 31, 23, 59, 59, 999999)
        else:
            end = datetime.datetime(self.now.year, self.now.month + 1, 1, 23, 59, 59, 999999) - datetime.timedelta(1)

        return start.strftime(self.template), end.strftime(self.template)

    def _get_year_period(self):
        """
        Returns beginning and an end for a year period.
        """
        start = datetime.datetime(self.now.year, 1, 1)
        end = datetime.datetime(self.now.year + 1, 1, 1, 23, 59, 59, 999999) - datetime.timedelta(1)

        return start.strftime(self.template), end.strftime(self.template)
