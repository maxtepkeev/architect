def init():
    import os
    from distutils.version import StrictVersion

    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        try:
            import django
            if StrictVersion(django.get_version()) < StrictVersion('1.7.0'):
                from django.conf import settings
            else:
                django.setup()
        except AttributeError:
            pass
