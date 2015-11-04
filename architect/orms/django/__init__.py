def init():
    try:
        import django
        django.setup()
    except AttributeError:
        pass
