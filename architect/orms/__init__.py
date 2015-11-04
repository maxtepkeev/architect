def init():
    """
    Some ORMs, e.g. Django, may require initialization to be performed, but only at some certain
    point, e.g. after some variables are set and so on, this function provides an ability to run
    this initialization for all supported ORMs automatically but only when needed by the caller
    """
    import os
    import pkgutil

    for _, name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if is_pkg:
            try:
                __import__(name, level=0)  # try to import globally and see if ORM is installed
            except ImportError:
                pass
            else:
                getattr(__import__(name, globals(), level=1), 'init', lambda: None)()  # if yes, run init() for this ORM
