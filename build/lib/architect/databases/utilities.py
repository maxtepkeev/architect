from datetime import date, datetime, timedelta


class Database(object):
    """Provides helpers for query execution via database cursor"""
    def __init__(self, cursor):
        if not cursor.connection.autocommit:
            cursor.connection.autocommit = True
        self.cursor = cursor

    def execute(self, sql):
        """Executes raw SQL for write operations"""
        return self.cursor.execute(sql)

    def select_one(self, sql, close=False):
        """Executes raw SQL for read operations and returns a single result"""
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        if close:
            self.cursor.close()

        return result[0] if result is not None else result

    def select_all(self, sql, as_dict=False, close=False):
        """Executes raw SQL for read operations and returns a full resultset either as dict or as a list of tuples"""
        self.cursor.execute(sql)

        if as_dict:
            result = [dict(zip([col[0] for col in self.cursor.description], row)) for row in self.cursor.fetchall()]
        else:
            result = self.cursor.fetchall()

        if close:
            self.cursor.close()

        return result


class DateTime(object):
    """Provides date and time calculations for some database backends"""
    def __init__(self, now, format='%Y-%m-%d %H:%M:%S'):
        self.now = datetime(now.year, now.month, now.day) if type(now) is date else now
        self.format = format

    def get_period(self, period):
        """Dynamically returns beginning and an end depending on the given period"""
        return getattr(self, '_get_{0}_period'.format(period))()

    def _get_day_period(self):
        """Returns beginning and an end for a day period"""
        start = self.now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = self.now.replace(hour=23, minute=59, second=59, microsecond=999999)

        return start.strftime(self.format), end.strftime(self.format)

    def _get_week_period(self):
        """Returns beginning and an end for a week period"""
        date_ = datetime(self.now.year, 1, 1)

        if date_.weekday() > 3:
            date_ = date_ + timedelta(7 - date_.weekday())
        else:
            date_ = date_ - timedelta(date_.weekday())

        days = timedelta(days=(int(self.now.strftime('%V')) - 1) * 7)

        fday = (date_ + days)
        lday = (date_ + days + timedelta(days=6)).replace(hour=23, minute=59, second=59, microsecond=999999)

        return fday.strftime(self.format), lday.strftime(self.format)

    def _get_month_period(self):
        """Returns beginning and an end for a month period"""
        fday = datetime(self.now.year, self.now.month, 1)

        if self.now.month == 12:
            lday = datetime(self.now.year, self.now.month, 31, 23, 59, 59, 999999)
        else:
            lday = datetime(self.now.year, self.now.month + 1, 1, 23, 59, 59, 999999) - timedelta(days=1)

        return fday.strftime(self.format), lday.strftime(self.format)

    def _get_year_period(self):
        """Returns beginning and an end for a year period"""
        fday = datetime(self.now.year, 1, 1)
        lday = datetime(self.now.year + 1, 1, 1, 23, 59, 59, 999999) - timedelta(days=1)

        return fday.strftime(self.format), lday.strftime(self.format)
