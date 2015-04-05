Changelog
---------

0.3.0 (2015-04-XX)
++++++++++++++++++

- Added: Documentation rewritten from scratch
- Added: Introduced completely new API (almost 80% of Architect code was rewritten from scratch).
  All functionality is now provided by an ``architect.install`` decorator which dynamically injects
  requested feature, e.g. partition, into a model under the ``architect`` namespace, e.g.
  ``model.architect.partition``. No more mixins, inheritance and nested classes with settings that
  pollute model's namespace. More information is available in the :doc:`docs </features/index>`
- Added: New ``operation`` feature which provide an abstraction layer to execute raw SQL statements
  which will work with any supported ORM, see :doc:`docs </features/operation>`
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
