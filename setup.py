import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test, DistutilsOptionError

for name in ('multiprocessing', 'pony'):  # https://bugs.python.org/issue15881
    try:
        __import__(name)
    except ImportError:
        pass


class NoseTests(test):
    user_options = test.user_options + [
        ('orm=', None, 'Sets ORM to run tests for'), ('db=', None, 'Sets DB to be used by ORM')]

    def initialize_options(self):
        test.initialize_options(self)
        self.db = None
        self.orm = None

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []
        self.test_suite = True
        if self.orm is not None:
            if self.db is None:
                raise DistutilsOptionError("--orm option can't be used without --db option")
            os.environ['DB'] = self.db
            os.environ[self.orm.upper()] = '1'

    def run_tests(self):
        import nose
        nose.run(argv=['nosetests'])
        if self.orm is not None:
            del os.environ['DB']
            del os.environ[self.orm.upper()]

tests_require = ['nose', 'coverage']

if sys.version_info[:2] < (3, 3):
    tests_require.append('mock')
    if sys.version_info[:2] == (3, 2):
        tests_require[1] = 'coverage<4.0'
    if sys.version_info[:2] == (2, 6):
        tests_require.append('unittest2')

exec(open('architect/version.py').read())

requirements = []

try:
    import argparse
except ImportError:
    requirements.append('argparse>=1.2.1')

setup(
    name='architect',
    version=globals()['__version__'],
    packages=find_packages(exclude=('tests', 'tests.*')),
    url='https://github.com/maxtepkeev/architect',
    license=open('LICENSE').read(),
    author='Max Tepkeev',
    author_email='tepkeev@gmail.com',
    description='A set of tools which enhances ORMs written in Python with more features',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    keywords='architect,django,pony,peewee,sqlalchemy,sqlobject,partition,partitioning,database,table',
    tests_require=tests_require,
    cmdclass={'test': NoseTests},
    zip_safe=False,
    install_requires=requirements,
    entry_points={'console_scripts': ['architect = architect.commands:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Database',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: SQL',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
