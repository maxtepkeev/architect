import sys
import functools
import contextlib

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from architect.commands import main


@contextlib.contextmanager
def capture():
    out, err, sys.stderr, sys.stdout = sys.stdout, sys.stderr, StringIO(), StringIO()

    try:
        main()
    except SystemExit:
        pass

    sys.stderr.seek(0)
    sys.stdout.seek(0)

    yield sys.stdout.read().strip(), sys.stderr.read().strip()

    sys.stdout = out
    sys.stderr = err


# For some reason unittest's skip decorator doesn't allow
# to skip a class which is very annoying. This one does.
def skip(reason):
    def decorator(test_item):
        @functools.wraps(test_item)
        def skip_wrapper(*args, **kwargs):
            raise unittest.SkipTest(reason)

        test_item = skip_wrapper
        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator

unittest.case.skip = skip
