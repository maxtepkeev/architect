Operations
==========

Sometimes there is a need to execute raw SQL statements, unfortunately different ORMs provide
different APIs to work with raw SQL. This feature creates an abstraction layer to execute raw
SQL statements which will work with any supported ORM. Operation feature is supported by Architect
for the following ORMs:

* `Django <https://www.djangoproject.com>`_ >= 1.4
* `Peewee <https://peewee.readthedocs.org>`_ >= 2.2.0
* `Pony <http://ponyorm.com>`_ >= 0.5.0
* `SQLAlchemy <http://www.sqlalchemy.org>`_ >= 0.8.0
* `SQLObject <http://www.sqlobject.org>`_ >= 1.5.0

This feature is used by all other Architect features internally and usually doesn't need to be
installed separately. If this is the only feature that will be used in the model it should be
installed like this:

.. code-block:: python

   import architect

   @architect.install('operation')
   class Model(object):
       pass

After the installation it can be accessed via ``Model.architect.operation``. Operation feature
provides the following methods:

.. automethodname:: architect.orms.bases.BaseOperationFeature.execute
.. automethodname:: architect.orms.bases.BaseOperationFeature.select_one
.. automethodname:: architect.orms.bases.BaseOperationFeature.select_all
