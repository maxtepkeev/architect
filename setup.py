from setuptools import setup, find_packages

exec(open('architect/version.py').read())

requirements = []

try:
    import argparse
except ImportError:
    requirements.append('argparse >= 1.2.1')


setup(
    name='architect',
    version=__version__,
    packages=find_packages(exclude=('tests', 'tests.*')),
    url='https://github.com/maxtepkeev/architect',
    license=open('LICENSE').read(),
    author='Max Tepkeev',
    author_email='tepkeev@gmail.com',
    description='A set of tools which enhances ORMs written in Python with more features',
    long_description=open('README.rst').read() + '\n\n' + open('CHANGELOG.rst').read(),
    keywords='architect,django,pony,peewee,sqlalchemy,sqlobject,partition,partitioning,database,table',
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
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
