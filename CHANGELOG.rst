Changelog
---------

0.5.4 (2016-07-04)
++++++++++++++++++

- Added: Django: `Issue #30 <https://github.com/maxtepkeev/architect/issues/30>`__ (Support for
  using database routers to determine correct database for a model in a multi database configuration)
- Fixed: Peewee: Table partitioning was broken in Peewee >= 2.7.4 due to Peewee API changes
- Fixed: PostgreSQL: Failed to partition a table if a reserved keyword was used as a column name

0.5.3 (2015-11-08)
++++++++++++++++++

- Added: Tests are now built-in into source package distributed via PyPI
- Fixed: Django: `Issue #21 <https://github.com/maxtepkeev/architect/issues/21>`__ (Unable to partition a
  model with non-lazy translations)

0.5.2 (2015-07-31)
++++++++++++++++++

- Fixed: PostgreSQL: `Issue #14 <https://github.com/maxtepkeev/architect/issues/14>`__ (Error when trying
  to save a record into a table if partitioned column value had special characters inside, using
  ``string_firstchars`` and ``string_lastchars`` partition subtypes)
- Fixed: PostgreSQL: `Issue #11 <https://github.com/maxtepkeev/architect/issues/11>`__ (Error when trying
  to save a record into a table that was partitioned by a column that can be ``NULL``, now if a column, that
  was used for partitioning, has ``NULL`` value it will be inserted into a special partition with ``_null``
  postfix)
- Fixed: SQLObject: Error when trying to partition a model with a field that has a ``default`` attribute
  set to some value

0.5.1 (2015-06-08)
++++++++++++++++++

- Fixed: `Issue #13 <https://github.com/maxtepkeev/architect/issues/13>`__ (MySQL support was broken
  in v0.5.0 released to PyPI)

0.5.0 (2015-05-08)
++++++++++++++++++

- Added: Django: `Issue #9 <https://github.com/maxtepkeev/architect/issues/9>`__ (Support for multiple
  databases)
- Added: Support for custom features, see `docs <http://architect.readthedocs.org/features/custom.html>`__
  for details
- Changed: ``dsn`` partition option renamed to ``db`` to cover more use cases
- Changed: ``DsnParseError`` exception renamed to ``OptionValueError`` to cover more use cases
- Fixed: Django: Error when trying to partition a model with Django <= 1.5 in debug mode
- Fixed: "No module named modulename.py" error when trying to specify model's module with .py extension
  at the end in partition command

0.4.0 (2015-04-18)
++++++++++++++++++

- Added: `wheel <http://wheel.readthedocs.org>`__ support
- Added: `SQLObject <http://www.sqlobject.org>`__ ORM support
- Added: PostgreSQL: New ``integer`` (thanks to `Nikolay Yarovoy <https://github.com/nickspring>`__),
  ``string_firstchars`` (thanks to `Dmitry Brytkov <https://github.com/dimoha>`__) and ``string_lastchars``
  range partition subtypes, see `docs <http://architect.readthedocs.org/features/partition/postgresql.html
  #range>`__ for details
- Changed: ``range`` partition option renamed to ``constraint`` to better suit new partition subtypes
- Changed: PostgreSQL: Triggers refactoring and speedups, don't forget to rerun ``partition`` command to
  apply new refactored triggers to the database
- Fixed: ``architect.uninstall`` decorator wasn't able to restore modified model methods under
  Python 3

0.3.0 (2015-04-05)
++++++++++++++++++

- Added: Documentation rewritten from scratch
- Added: Introduced completely new API (almost 80% of Architect code was rewritten from scratch).
  All functionality is now provided by an ``architect.install`` decorator which dynamically injects
  requested feature, e.g. partition, into a model under the ``architect`` namespace, e.g.
  ``model.architect.partition``. No more mixins, inheritance and nested classes with settings that
  pollute model's namespace. More information is available in the `docs <http://architect.readthedocs.org
  /features/index.html>`__
- Added: New ``operation`` feature which provide an abstraction layer to execute raw SQL statements
  which will work with any supported ORM, see `docs <http://architect.readthedocs.org/features/
  operation.html>`__
- Fixed: `Issue #8 <https://github.com/maxtepkeev/architect/issues/8>`__ (``cannot import name
  string_literal`` error with PonyORM and PyMySQL if ``pymysql.install_as_MySQLdb()`` was used)
- Fixed: `Issue #7 <https://github.com/maxtepkeev/architect/pull/7>`__ (SQLite dummy backend was
  completely broken)
- Fixed: `Issue #4 <https://github.com/maxtepkeev/architect/pull/4>`__ (``autocommit cannot be
  used inside a transaction`` error with Django if a model was used inside ``with
  transaction.atomic()`` block)
- Fixed: `Issue #2 <https://github.com/maxtepkeev/architect/issues/2>`__ (``partition``
  command was unable to find module with models to partition)
- Fixed: `Issue #1 <https://github.com/maxtepkeev/architect/issues/1>`__ (``relation already
  exists`` error when trying to insert data into non-existent partition simultaneously from
  several queries) (thanks to `Daniel Kontsek <https://github.com/dn0>`__)

0.2.0 (2014-07-19)
++++++++++++++++++

- Added: MySQL range partitioning support

0.1.0 (2014-07-13)
++++++++++++++++++

- Initial release
