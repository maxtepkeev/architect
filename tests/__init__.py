import os
import sys
from contextlib import contextmanager

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

from architect.commands import main


@contextmanager
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
