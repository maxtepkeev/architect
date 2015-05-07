Custom features
===============

.. versionadded:: 0.5.0

Architect supports custom features which can be used to add completely new functionality to
a model or to redefine some built-in feature's behaviour. A completely new feature can be
created and installed as the following:

.. code-block:: python

   from architect.orms.bases import BaseFeature

   class CustomFeature(BaseFeature):
       orm = 'django'
       name = 'my_feature'
       decorate = ('bar',)

       def foo(self):
           """Does something with a model"""
           pass

       @staticmethod
       def _decorate_bar(method):
           """Decorates model's bar method"""
           def wrapper(instance, *args, **kwargs):
               # Do something before method invocation
               method(instance, *args, **kwargs)
               # Do something after method invocation
           return wrapper

   @architect.install('my_feature')
   class Model(object):
       pass

To be considered a feature class, a class should inherit from a ``BaseFeature`` or any other
class that itself inherits from a ``BaseFeature`` and implement ``orm`` and ``name`` attributes.
``orm`` attribute is used to identify to which ORM this feature belongs to and ``name`` attribute
is used by Architect to identify this feature in an internal feature registry. If a feature class
should be considered a base for other feature classes simply don't set an ``orm`` attribute and
it will defaults to ``None`` which tells Architect that this is a base feature class.

.. raw:: html

   <h2 id="api">
       API
       <a class="headerlink" href="#api" title="Permalink to this headline">¶</a>
   </h2>

``BaseFeature`` class provides the following methods and attributes:

.. autoattribute-name-only:: architect.orms.bases.BaseFeature.orm
.. autoattribute-name-only:: architect.orms.bases.BaseFeature.name
.. autoattribute-name-only:: architect.orms.bases.BaseFeature.decorate
.. autoattribute-name-only:: architect.orms.bases.BaseFeature.dependencies
.. automethod-name-only:: architect.orms.bases.BaseFeature.__init__
