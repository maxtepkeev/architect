Table partitioning
==================

Table partitioning is a division of one table into several tables, called partitions, which still
represent original table. This is usually done for manageability, performance or availability reasons.
If you are unsure whether you need partitioning or not, then you almost certainly don't need it.
Table partitioning feature is supported by Architect for the following ORMs:

* `Django <https://www.djangoproject.com>`_ >= 1.4
* `Peewee <https://peewee.readthedocs.org>`_ >= 2.2.0
* `Pony <http://ponyorm.com>`_ >= 0.5.0
* `SQLAlchemy <http://www.sqlalchemy.org>`_ >= 0.8.0

To use this feature, define the model as usual and create a table for it in the database using the
usual tools that your ORM provides. After the table was created, this feature can be installed into
the model as the following:

.. code-block:: python

   import architect

   @architect.install('partition', **options)
   class Model(object):
       pass

where ``options`` are:

- ``type`` (required). Partition type, currently accepts the following:

  * range

- ``subtype`` (required). Partition subtype, currently used only when ``type`` is set to ``range`` and
  accepts the following:

  * date

- ``range`` (required). How often a new partition will be created, currently accepts the following:

  * day
  * week
  * month
  * year

- ``column`` (required). Column, which value will be used to determine which partition record belongs to.
- ``dsn`` (optional). Data Source Name in the form of dialect://user:pass@host/database. Currently needed
  only for SQLAlchemy.

.. note::

   Using this feature with a Django ORM, run the following command before moving to next step,
   substituting ``mysite.settings`` to the real path of the Django settings module:

   .. code-block:: bash

      $ export DJANGO_SETTINGS_MODULE=mysite.settings

After the feature has been installed into the model, run the following console command:

.. code-block:: bash

   $ architect partition --module path.to.the.model.module

That's it. Now, when a new record will be inserted, a value from column, specified in the ``column``
setting will be used to determine into what partition the data should be saved. Keep in mind that if
new partitioned models are added or any settings are changed in existing partitioned models, the
partition command should be rerun, otherwise the database won't know about this changes.

Implementation details
----------------------

PostgreSQL
++++++++++

PostgreSQL's partitioning implementation in Architect is done purely at the database level. That means
that Architect creates several triggers and functions and inserts them directly into the database, so
even if you issue direct insert statement from database console and not from the ORM, everything will work
as expected and record will be inserted into the correct partition, if partition doesn't exist, it will
be created for you automatically. Also partitions may be created in any order and not only from lower to
higher.

Supported partitioning types
****************************

* Range partitioning by date/datetime for the following periods:

  - day
  - week
  - month
  - year

Limitations
***********

* Not all partitioning types are supported. New types will be added in future releases of Architect.

MySQL
+++++

MySQL's partitioning implementation in Architect is done in a mixed way, half at the python level and
half at the database level. Unfortunately MySQL doesn't support dynamic sql in triggers or functions/
procedures that are called within triggers, so the only way to create partitions automatically is to
calculate everything at the python level, then to create needed sql statements based on calculations
and issue that statements into the database.

Supported partitioning types
****************************

* Range partitioning by date/datetime for the following periods:

  - day
  - week
  - month
  - year

Limitations
***********

* Not all partitioning types are supported. New types will be added in future releases of Architect.
* New partitions can be created only from lower to higher, you can overcome this with MySQL's special
  command REORGANIZE PARTITION which you have to issue from the database console. You can read more
  about it at the MySQL's documentation. We plan to remove this limitation in one of the future releases
  of Architect.
