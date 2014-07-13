Peewee
======

Requirements
------------

* `Peewee <https://peewee.readthedocs.org>`_ >= 2.2.0

Configuration
-------------

Create the model which will represent the partitioned table as usual and `create <http://peewee.readthe
docs.org/en/latest/peewee/api.html#Model.create_table>`_ a table for it using ``YourModel.create_table()``.
After that make the following changes to the model:

1. In the file where the model is defined add the following import statement:

.. code-block:: python

    from architect.orms.peewee.mixins import PartitionableMixin

2. Add ``PartitionableMixin`` to the model, to do that change:

.. code-block:: python

    class YourModelName(Model):

to:

.. code-block:: python

    class YourModelName(PartitionableMixin, Model):

3. Add a ``PartitionableMeta`` class to the model with a few settings (keep in mind that this is
   just an example configuration, you have to enter values which represent your exact needs, see below):

.. code-block:: python

    class YourModelName(PartitionableMixin, Model):
        class PartitionableMeta:
            partition_type = 'range'
            partition_subtype = 'date'
            partition_range = 'month'
            partition_column = 'added'

4. Lastly initialize some database stuff, to do that execute the following command:

.. code-block:: bash

    $ architect partition --module path.to.the.model.module

Now, when a new record will be inserted, a value from ``added`` column will be used to determine into
what partition the data should be saved. Keep in mind that if new partitioned models are added or any
settings are changed in existing partitioned models, the command from step 4 should be rerun, otherwise
the database won't know about this changes.

Available settings
------------------

Model settings
~~~~~~~~~~~~~~

All the following model settings should be defined inside model's ``PartitionableMeta`` class:

partition_type
++++++++++++++

Partition type that will be used on the model, currently accepts the following:

* range

partition_subtype
+++++++++++++++++

Partition subtype that will be used on the model, currently used only when ``partition_type`` is set to
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
