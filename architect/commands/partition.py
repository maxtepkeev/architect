from architect.orms import BasePartitionableMixin
from architect.exceptions import ImportProblemError

arguments = [
    {('-m', '--module'): {
        'dest': 'module',
        'required': True,
        'help': 'path to the module with models to be partitioned'
    }},
    {('-c', '--connection'): {
        'dest': 'connection',
        'required': False,
        'metavar': 'DSN',
        'help': 'database connection string in the form of dsn'
    }}
]


def run(args):
    """Partition command. Prepares models from the specified module for partitioning"""
    names = []
    mod = args['module']

    try:
        mod_clss = filter(lambda obj: isinstance(obj, type), __import__(mod, fromlist=mod).__dict__.values())
    except ImportError as e:
        raise ImportProblemError(str(e))

    for cls in mod_clss:
        if issubclass(cls, BasePartitionableMixin) and not 'architect.orms' in cls.__module__:
            model_instance = cls.get_empty_instance(args['connection'])
            model_instance.get_partition().prepare()
            names.append(cls.__name__)

    if not names:
        return 'unable to find any partitionable models in a module: {0}'.format(mod)
    else:
        return 'successfully (re)configured the database for the following models: {0}'.format(', '.join(names))
