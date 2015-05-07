"""
Partition command implementation.
"""

from ..exceptions import ImportProblemError

arguments = [
    {('-m', '--module'): {
        'dest': 'module',
        'required': True,
        'help': 'path to the module with models to be partitioned'
    }}
]


def run(args):
    """
    Prepares models from specified module for partitioning.

    :param dictionary args: (required). Dictionary of command arguments.
    """
    names = []
    module = args['module'][:-3] if args['module'].endswith('.py') else args['module']

    try:
        module_clss = filter(lambda obj: isinstance(obj, type), __import__(module, fromlist=module).__dict__.values())
    except ImportError as e:
        raise ImportProblemError(str(e))

    for cls in module_clss:
        if hasattr(cls, 'architect') and hasattr(cls.architect, 'partition'):
            cls.architect.partition.get_partition().prepare()
            names.append(cls.__name__)

    if not names:
        return 'unable to find any partitionable models in a module: {0}'.format(module)
    else:
        return 'successfully (re)configured the database for the following models: {0}'.format(', '.join(names))
