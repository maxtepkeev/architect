"""
Tests decorators only.
"""

from . import unittest, mock

from architect import install, uninstall
from architect.orms.bases import BaseFeature


class BaseDecoratorTestCase(object):
    def setUp(self):
        with mock.patch('pkgutil.iter_modules') as modules:
            modules.return_value = [(None, 'foo', True)]
            self.foo_feature = type('FooFeature', (BaseFeature,), dict(orm='foo', name='foo'))
            self.bar_feature = type('BarFeature', (BaseFeature,), dict(orm='foo', name='bar', dependencies=('foo',)))

        spec = ['FooFeature', 'BarFeature']
        foo = mock.Mock(features=mock.Mock(spec=spec, FooFeature=self.foo_feature, BarFeature=self.bar_feature))
        patcher = mock.patch.dict('sys.modules', {
            'architect.orms.foo': foo,
            'architect.orms.foo.features': foo.features
        })
        patcher.start()
        self.addCleanup(patcher.stop)

        self.meta = type('Metaclass', (type,), {})
        self.model = type('Model', (self.meta('NewBase', (object,), {}),), {'save': lambda *args, **kwargs: 'save'})


class InstallDecoratorTestCase(BaseDecoratorTestCase, unittest.TestCase):
    def test_merges_several_features(self):
        self.model = install('bar', orm='foo')(self.model)
        self.model = uninstall('foo')(self.model)
        self.model = install('foo', orm='foo')(self.model)
        self.assertIn('foo', self.model.architect.__dict__)
        self.assertIn('bar', self.model.architect.__dict__)

    def test_gathers_original_method(self):
        self.bar_feature.decorate = ('save',)
        self.bar_feature._decorate_save = staticmethod(lambda method: lambda *args, **kwargs: None)
        self.model = install('bar', orm='foo')(self.model)
        self.childmodel = type('ChildModel', (self.model,), {})
        self.childmodel = install('bar', orm='foo')(self.childmodel)
        self.assertEqual(self.model.save.original(self.model()), 'save')
        self.assertEqual(self.childmodel.save.original(self.childmodel()), 'save')

    def test_register_hooks(self):
        self.foo_feature.register_hooks = staticmethod(lambda model: setattr(model, 'foo', 'foo'))
        self.model = install('foo', orm='foo')(self.model)
        self.assertEqual(self.model.foo, 'foo')

    def test_dynamically_changes_model_object(self):
        self.model = install('foo', orm='foo')(self.model)
        obj1 = self.model().architect.foo.model_obj
        self.assertEqual(self.model.__dict__['architect'].map[self.model]['features']['foo'].model_obj, obj1)
        obj2 = self.model().architect.foo.model_obj
        self.assertEqual(self.model.__dict__['architect'].map[self.model]['features']['foo'].model_obj, obj2)

    def test_raises_orm_error(self):
        from architect.exceptions import ORMError
        self.assertRaises(ORMError, lambda: install('partition', orm='bar')(self.model))

    def test_raises_feature_install_error(self):
        from architect.exceptions import FeatureInstallError
        self.assertRaises(FeatureInstallError, lambda: install('foobar', orm='foo')(self.model))

    def test_raises_method_autodecorate_error(self):
        from architect.exceptions import MethodAutoDecorateError as MADError
        self.foo_feature.decorate = ('save',)
        self.assertRaises(MADError, lambda: install('foo', orm='foo')(mock.Mock(spec=['__name__'])))


class UninstallDecoratorTestCase(BaseDecoratorTestCase, unittest.TestCase):
    def test_successful_uninstall(self):
        self.model = install('bar', orm='foo')(self.model)
        self.assertIn('foo', self.model.architect.__dict__)
        self.assertIn('bar', self.model.architect.__dict__)
        uninstall('bar')(self.model)
        self.assertNotIn('foo', self.model.architect.__dict__)
        self.assertNotIn('bar', self.model.architect.__dict__)

    def test_uninstall_restores_decorated_method(self):
        self.foo_feature.decorate = ('save',)
        self.foo_feature._decorate_save = staticmethod(lambda method: lambda *args, **kwargs: None)
        self.model = install('foo', orm='foo')(self.model)
        self.assertIsNone(self.model.save(self.model()))
        self.model = uninstall('foo')(self.model)
        self.assertEqual(self.model.save(self.model()), 'save')

    def test_raises_feature_uninstall_error(self):
        from architect.exceptions import FeatureUninstallError
        self.model = install('foo', orm='foo')(self.model)
        self.assertRaises(FeatureUninstallError, lambda: uninstall('bar')(self.model))
