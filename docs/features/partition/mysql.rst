MySQL
=====

MySQL's partitioning implementation in Architect is done in a mixed way, half at the python level and
half at the database level. Unfortunately MySQL doesn't support dynamic sql in triggers or functions /
procedures that are called within triggers, so the only way to create partitions automatically is to
calculate everything at the python level, then to create needed sql statements based on calculations
and issue that statements into the database.

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

Limitations
-----------

* Not all partitioning types are supported. New ones will be added in next releases of Architect.
* New partitions can be created only from lower to higher, you can overcome this with MySQL's special
  command REORGANIZE PARTITION which you have to issue from the database console. You can read more
  about it at the MySQL's documentation. We plan to remove this limitation in one of the future releases
  of Architect.
