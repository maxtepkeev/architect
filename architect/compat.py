"""
Python compatibility layer.
"""

import sys

py2 = sys.version_info[0] == 2
py3 = sys.version_info[0] == 3

if py2:
    pass
elif py3:
    pass


def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.
    """
    class MetaClass(meta):
        def __new__(cls, name, this_bases, dct):
            return meta(name, bases, dct)
    return type.__new__(MetaClass, 'temporary_class', (), {})
