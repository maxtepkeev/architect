Table Partitioning
==================

.. The reason we are using raw html for paragraphs here is because otherwise they will be inserted
   into the left menu and we don't want that. At the time of writing there is no other way to do
   what we want other than this ugly one.

Table partitioning is a division of one table into several tables, called partitions, which still
represent original table. This is usually done for manageability, performance or availability reasons.
If you are unsure whether you need partitioning or not, then you almost certainly don't need it.

.. raw:: html

    <h2 id="postgresql">
        PostgreSQL
        <a class="headerlink" href="#postgresql" title="Permalink to this headline">¶</a>
    </h2>

PostgreSQL's partitioning implementation in Architect is done purely at the database level. That means
that Architect creates several triggers and functions and inserts them directly into the database, so
even if you issue direct insert statement from database console and not from the ORM, everything will work
as expected and record will be inserted into the correct partition, if partition doesn't exist, it will
be created for you automatically. Also partitions may be created in any order and not only from lower to
higher.

.. raw:: html

    <h3 id="postgresql-partitioning-types">
        Supported partitioning types
        <a class="headerlink" href="#postgresql-partitioning-types" title="Permalink to this headline">¶</a>
    </h3>

* Range partitioning by date/datetime for the following periods:

  - day
  - week
  - month
  - year

.. raw:: html

    <h3 id="postgresql-limitations">
        Limitations
        <a class="headerlink" href="#postgresql-limitations" title="Permalink to this headline">¶</a>
    </h3>

* Not all partitioning types are supported. New types will be added in future releases of Architect.

.. raw:: html

    <h2 id="mysql">
        MySQL
        <a class="headerlink" href="#mysql" title="Permalink to this headline">¶</a>
    </h2>

MySQL's partitioning implementation in Architect is done in a mixed way, half at the python level and
half at the database level. Unfortunately MySQL doesn't support dynamic sql in triggers or functions
that are called within triggers, so the only way to create partitions automatically is to calculate
everything at the python level, then to create needed sql statements based on calculations and issue
that statement into the database.

.. raw:: html

    <h3 id="mysql-partitioning-types">
        Supported partitioning types
        <a class="headerlink" href="#mysql-partitioning-types" title="Permalink to this headline">¶</a>
    </h3>

* Range partitioning by date/datetime for the following periods:

  - day
  - week
  - month
  - year

.. raw:: html

    <h3 id="mysql-limitations">
        Limitations
        <a class="headerlink" href="#mysql-limitations" title="Permalink to this headline">¶</a>
    </h3>

* Not all partitioning types are supported. New types will be added in future releases of Architect.
* New partitions can be created only from lower to higher, you can overcome this with MySQL's special
  command REORGANIZE PARTITION which you have to issue from the database console. You can read more
  about it at the MySQL's documentation. We plan to remove this limitation in one of the future releases
  of Architect.

.. raw:: html

    <h2 id="supported-orms">
        Supported ORMs
        <a class="headerlink" href="#supported-orms" title="Permalink to this headline">¶</a>
    </h2>

.. toctree::
    :maxdepth: 1

    django
    peewee
    pony
    sqlalchemy
