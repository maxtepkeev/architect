PostgreSQL
==========

PostgreSQL's partitioning implementation in Architect is done purely at the database level. That means
that Architect creates several triggers and functions and inserts them directly into the database, so
even if you issue direct insert statement from database console and not from the ORM, everything will work
as expected and record will be inserted into the correct partition, if partition doesn't exist, it will
be created for you automatically. Also partitions may be created in any order and not only from lower to
higher.

Supported types
---------------

range
+++++

Range partitioning maps data to partitions based on ranges of values of the partitioning column. It is
the most common type of partitioning and is often used with dates or integers, but it can be used with
other types as well. Architect supports several subtypes for range partitioning type.

date
****

Date subtype is used to partition table by date ranges. For example, the y2005m01 partition would contain
rows with partitioning column values from 2005-01-01 to 2005-01-31. This subtype has the following constraints:

- day - a new partition will be created every day
- week - a new partition will be created every week
- month - a new partition will be created every month
- year - a new partition will be created every year

.. code-block:: python

   import architect

   @architect.install('partition', type='range', subtype='date', constraint='month', column='columnname')
   class Model(object):
       pass

integer
*******

.. versionadded:: 0.4.0

Integer subtype is used to partition table by integer ranges, for example, one may want to create
a new partition for every 100 rows of data, i.e. rows with id 37 and id 68 will go to partition which collects
ids from 1 to 100. Integer subtype also supports negative and zero values, so it can be used not only with
ids but with any integer column, signed or unsigned.

.. code-block:: python

   import architect

   @architect.install('partition', type='range', subtype='integer', constraint='100', column='columnname')
   class Model(object):
       pass

string_firstchars
*****************

.. versionadded:: 0.4.0

String firstchars subtype is used to partition table by selecting first N characters from a string, for
example, we want to have partitions based on the first 5 characters of a string, i.e. strings "foobar" and
"foobarbaz" will go to partition named "fooba", but string "foo" will go to its own partition "foo" because
it doesn't have enough characters, string "yadayada" will go to partition "yaday" etc.

.. code-block:: python

   import architect

   @architect.install('partition', type='range', subtype='string_firstchars', constraint='5', column='columnname')
   class Model(object):
       pass

string_lastchars
****************

.. versionadded:: 0.4.0

This subtype is the same as ``string_firstchars`` except that it counts from the end of string and not
from the beginning, i.e. string "foobar" will go to partition "oobar", string "foobarbaz" to partition
"arbaz" etc.

.. code-block:: python

   import architect

   @architect.install('partition', type='range', subtype='string_lastchars', constraint='5', column='columnname')
   class Model(object):
       pass

Limitations
-----------

* Not all partitioning types are supported. New ones will be added in next releases of Architect.
