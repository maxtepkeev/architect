Table partitioning
==================

Table partitioning is a division of one table into several tables, called partitions, which still
represent original table. This is usually done for manageability, performance or availability reasons.
If you are unsure whether you need partitioning or not, then you almost certainly don't need it.

To use this feature, define the model as usual and create a table for it in the database using the
usual tools that your ORM provides. After the table was created, this feature can be installed into
the model as the following:

.. code-block:: python

   import architect

   @architect.install('partition', **options)
   class Model(object):
       pass

where ``options`` are:

- ``type`` (required). Partition type, e.g. ``range``, ``list`` etc
- ``subtype`` (required). Partition subtype, e.g. ``date``, ``integer`` etc
- ``constraint`` (required). What data fits into partition, e.g. ``day``, ``5`` (every 5 items) etc
- ``column`` (required). Column, which value determines which partition record belongs to
- ``db`` (optional). Currently used with:

  * Django - only for specifying other database name instead of ``default``.
  * SQLAlchemy - required if model's ``metadata`` is not bound to any engine, should be set in the form of
    Data Source Name, e.g. dialect://user:pass@host/database.

Above options can take different values depending on the database type because different databases support
different partition types, subtypes etc. To find out which values can be set for the above options choose
the database type which you currently use from the list below:

.. toctree::
   :maxdepth: 1

   postgresql
   mysql

.. note::

   Using this feature with a Django ORM, run the following command before moving to next step,
   substituting ``mysite.settings`` to the real path of the Django settings module:

   .. code-block:: bash

      $ export DJANGO_SETTINGS_MODULE=mysite.settings

After the feature has been installed into the model, run the following console command:

.. code-block:: bash

   $ architect partition --module path.to.the.model.module

That's it. Now, when a new record will be inserted, a value from column, specified in the ``column``
option will be used to determine into what partition the data should be saved. Keep in mind that if
new partitioned models are added or any settings are changed in existing partitioned models, the
partition command should be rerun, otherwise the database won't know about this changes.

.. raw:: html

   <h2 id="api">
       API
       <a class="headerlink" href="#api" title="Permalink to this headline">¶</a>
   </h2>

After the installation partition feature can be accessed via ``Model.architect.partition``, though it
usually doesn't need to be accessed directly because everything is done automatically. It provides the
following methods:

.. autoattribute-name-only:: architect.orms.bases.BasePartitionFeature.model_meta
.. automethod-name-only:: architect.orms.bases.BasePartitionFeature.get_partition

   This object provides the following methods:

   .. automethod-name-only:: architect.databases.bases.BasePartition.prepare
   .. automethod-name-only:: architect.databases.bases.BasePartition.create
   .. automethod-name-only:: architect.databases.bases.BasePartition.exists
