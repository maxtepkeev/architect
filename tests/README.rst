Running tests
=============

To run tests you will need these packages:

* coverage
* nose
* mock

For your convenience they are all listed in the ``requirements.txt`` file in this directory.
If you are running Python 3.4+ ``mock`` already exists in the standard library as a part of
unittest package so you don't need to install it. For Python 2.6 you also need to install
``unittest2`` package. After all dependencies are installed you can run tests with this command:

.. code-block:: bash

    $ nosetests --with-coverage --cover-erase --cover-package=architect

Alternatively, starting from v0.5.3 you can use

.. code-block:: bash

    $ python setup.py test --orm=ORM --db=DB

where ORM is one of the supported ORMs (django, peewee, pony, sqlalchemy, sqlobject) and DB is one
of the supported databases (mysql, pgsql, sqlite) or "all" if you want to test all databases in
one go. Using the above command will automatically install all the dependencies needed for running
tests, so you don't have to do it by hand.
