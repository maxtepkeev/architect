Features
========

.. The reason we are using raw html for paragraphs here is because otherwise they will be inserted
   into the left menu and we don't want that. At the time of writing there is no other way to do
   what we want other than this ugly one.

Architect has a concept of "features". A feature in Architect is something that can somehow enhance
the ORM Architect is used with, e.g. table partitioning. Architect provides a single interface to
all of its features despite of the ORM being used.

.. raw:: html

   <h2 id="install">
       install
       <a class="headerlink" href="#install" title="Permalink to this headline">¶</a>
   </h2>

All features in Architect are installed into models using ``install`` decorator. An ``install``
decorator in it's general form can be written as the following:

.. code-block:: python

   import architect

   @architect.install(feature, **options)
   class Model(object):
       pass

where ``feature`` is the feature name as a string which should be installed into the model class and
``options`` are the options that this feature takes (if any) in the form of keyword arguments. If a
model wants to use several features, this can easily be done with applying several decorators at once,
like this:

.. code-block:: python

   import architect

   @architect.install(feature1, **options1)
   @architect.install(feature2, **options2)
   @architect.install(feature3, **options3)
   class Model(object):
       pass

All installed features can be found inside ``architect`` namespace inside the model, e.g.:

.. code-block:: python

   >>> print(dir(Model.architect))
   ['__class__', '__dict__', 'feature1', 'feature2', 'feature3']

This provides 100% non-conflicting behaviour with all ORMs and other 3rd party packages.

.. note::

   Architect tries its best to automatically determine what ORM it is being used with, however there
   can be situations when it can fail to properly do that. To help Architect, one can pass an ``orm``
   option to the ``install`` decorator and set it to the needed ORM.

.. raw:: html

   <h2 id="uninstall">
       uninstall
       <a class="headerlink" href="#uninstall" title="Permalink to this headline">¶</a>
   </h2>

Under some circumstances a model might not need one or all of the installed features anymore, one
example can be a model inheritance, where the parent model has a feature installed and a child model
doesn't want to use it. A feature can be easily uninstalled from a model using ``uninstall`` decorator:

.. code-block:: python

   import architect

   @architect.uninstall(feature)
   class ChildModel(object):
       pass

where a ``feature`` is a feature name as a string which was installed before.

.. toctree::
   :hidden:
   :maxdepth: 1

   operation
   partition/index
   custom
