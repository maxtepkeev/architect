from . import unittest, mock

from architect import install, uninstall


class BaseDecoratorTestCase(object):
    def setUp(self):
        self.meta = type('Metaclass', (type,), {})
        self.model = type('Model', (self.meta('NewBase', (object,), {}),), {'save': lambda *args, **kwargs: 'save'})
        self.model = install('partition', orm='django')(self.model)


class InstallDecoratorTestCase(BaseDecoratorTestCase, unittest.TestCase):
    def test_merges_several_features(self):
        self.model = uninstall('operation')(self.model)
        self.model = install('operation', orm='django')(self.model)
        self.assertIn('partition', self.model.architect.__dict__)
        self.assertIn('operation', self.model.architect.__dict__)

    def test_gathers_original_method(self):
        self.childmodel = type('ChildModel', (self.model,), {})
        self.childmodel = install('partition', orm='django')(self.childmodel)
        self.assertEqual(self.model.save.original(self.model()), 'save')
        self.assertEqual(self.childmodel.save.original(self.childmodel()), 'save')

    def test_register_hooks(self):
        from architect.orms.bases import BaseFeature
        foo = mock.Mock()
        modules = {'architect.orms.foo': foo, 'architect.orms.foo.features': foo.features}
        with mock.patch.dict('sys.modules', modules):
            from architect.orms.foo import features
            features.FooFeature = type('Foo', (BaseFeature,), {
                'register_hooks': staticmethod(lambda model: setattr(model, 'foo', 'foo'))
            })
            self.model = install('foo', orm='foo')(self.model)
            self.assertEqual(self.model.foo, 'foo')

    def test_raises_orm_error(self):
        from architect.exceptions import ORMError
        self.assertRaises(ORMError, lambda: install('partition', orm='foo')(self.model))

    def test_raises_feature_install_error(self):
        from architect.exceptions import FeatureInstallError
        self.assertRaises(FeatureInstallError, lambda: install('foo', orm='django')(self.model))

    def test_raises_method_autodecorate_error(self):
        from architect.exceptions import MethodAutoDecorateError as MADError
        self.assertRaises(MADError, lambda: install('partition', orm='django')(mock.Mock(spec=['__name__'])))


class UninstallDecoratorTestCase(BaseDecoratorTestCase, unittest.TestCase):
    def test_successful_uninstall(self):
        self.assertIn('partition', self.model.architect.__dict__)
        self.assertIn('operation', self.model.architect.__dict__)
        uninstall('partition')(self.model)
        self.assertNotIn('partition', self.model.architect.__dict__)
        self.assertNotIn('operation', self.model.architect.__dict__)

    def test_raises_feature_uninstall_error(self):
        from architect.exceptions import FeatureUninstallError
        self.assertRaises(FeatureUninstallError, lambda: uninstall('foo')(self.model))
