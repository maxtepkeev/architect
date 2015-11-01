import os
import pkgutil

# Some ORMs, e.g Django, requires some setup to be performed before one can use them
for _, name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
    if is_pkg:
        try:
            __import__(name, level=0)  # try to import globally and see if ORM is installed
        except ImportError:
            pass
        else:
            __import__(name, globals(), level=1)  # if yes, run Architect's init code for this ORM
