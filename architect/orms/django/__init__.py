def init():
    import os

    if 'DJANGO_SETTINGS_MODULE' in os.environ:
        try:
            import django
            django.setup()
        except AttributeError:
            pass
