"""
Defines registry metaclass and helper attributes.
"""

import re
import os
import pkgutil

from ..exceptions import ORMError


registry = {}


class Registrar(type):
    """
    A feature that implements this metaclass, e.g. all features that inherit from BaseFeature,
    will be added to feature registry if it defines name and orm attributes, otherwise it will
    be treated as a base (abstract) feature and won't be registered.
    """
    orms = []  # list of ORMs for which a built-in features module was loaded

    def __new__(mcs, name, bases, attrs):
        # It is possible to automatically determine ORM for built-in Architect features
        orm = re.match('architect.orms.(\w+).features', attrs.get('__module__', ''))

        if orm is not None:
            attrs['orm'] = orm.group(1)
            mcs.orms.append(orm.group(1))

        feature_cls = super(Registrar, mcs).__new__(mcs, name, bases, attrs)
        orms = [mod_name for _, mod_name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]) if is_pkg]

        if feature_cls.orm is None:  # This is a base class and it shouldn't be registered
            return feature_cls
        elif feature_cls.orm not in orms:
            raise ORMError(current=feature_cls.orm, model=name, allowed=orms)

        registry.setdefault(feature_cls.orm, {})[feature_cls.name] = feature_cls
        return feature_cls
