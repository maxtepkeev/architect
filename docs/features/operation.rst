Operations
==========

Sometimes there is a need to execute raw SQL statements, unfortunately different ORMs provide
different APIs to work with raw SQL. This feature creates an abstraction layer to execute raw
SQL statements which will work with any supported ORM. It is used by all other Architect
features internally and usually doesn't need to be installed separately. However, if this is
the only feature that will be used in the model it can be installed like this:

.. code-block:: python

   import architect

   @architect.install('operation')
   class Model(object):
       pass

.. raw:: html

   <h2 id="api">
       API
       <a class="headerlink" href="#api" title="Permalink to this headline">¶</a>
   </h2>

After the installation operation feature can be accessed via ``Model.architect.operation``. It
provides the following methods:

.. automethod-name-only:: architect.orms.bases.BaseOperationFeature.execute
.. automethod-name-only:: architect.orms.bases.BaseOperationFeature.select_one
.. automethod-name-only:: architect.orms.bases.BaseOperationFeature.select_all
