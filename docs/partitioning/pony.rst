Pony
====

Requirements
------------

* `Pony <http://ponyorm.com>`_ >= 0.4.8

Configuration
-------------

Define the entity which will represent the partitioned table as usual and `create <http://doc.ponyorm.com/
firststeps.html#mapping-entities-to-database-tables>`_ a table for it using
``db.generate_mapping(create_tables=True)``. After that make the following changes to the model:

1. In the file where the entity is defined add the following import statement:

.. code-block:: python

    from architect.orms.pony.mixins import PartitionableMixin

2. Add ``PartitionableMixin`` to the entity, to do that change:

.. code-block:: python

    class YourEntityName(db.Entity):

to:

.. code-block:: python

    class YourEntityName(PartitionableMixin, db.Entity):

3. Add a ``PartitionableMeta`` class to the entity with a few settings (keep in mind that this is
   just an example configuration, you have to enter values which represent your exact needs, see below):

.. code-block:: python

    class YourEntityName(PartitionableMixin, db.Entity):
        class PartitionableMeta:
            partition_type = 'range'
            partition_subtype = 'date'
            partition_range = 'month'
            partition_column = 'added'

4. Lastly initialize some database stuff, to do that execute the following command:

.. code-block:: bash

    $ architect partition --module path.to.the.entity.module

Now, when a new record will be inserted, a value from ``added`` column will be used to determine into
what partition the data should be saved. Keep in mind that if new partitioned entities are added or any
settings are changed in existing partitioned entities, the command from step 4 should be rerun, otherwise
the database won't know about this changes.

Available settings
------------------

Entity settings
~~~~~~~~~~~~~~~

All the following entity settings should be defined inside entity's ``PartitionableMeta`` class:

partition_type
++++++++++++++

Partition type that will be used on the entity, currently accepts the following:

* range

partition_subtype
+++++++++++++++++

Partition subtype that will be used on the entity, currently used only when ``partition_type`` is set to
``range`` and accepts the following:

* date

partition_range
+++++++++++++++

How often a new partition will be created, currently accepts the following:

* day
* week
* month
* year

partition_column
++++++++++++++++

Column, which value will be used to determine which partition record belongs to
