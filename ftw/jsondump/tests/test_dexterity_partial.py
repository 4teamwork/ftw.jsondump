from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from zope.component import getMultiAdapter


class TestDexterityPatial(FtwJsondumpTestCase):

    def test_field_dottednames_enabled_by_default(self):
        item = create(Builder('dx item').titled(u'Foo'))
        partial = getMultiAdapter((item, None), IPartial, name="fields")
        self.assertDictContainsSubset(
            {u'plone.app.dexterity.behaviors.metadata.IBasic.title': u'Foo'},
            partial(config={}))

    def test_disabling_field_dottednames(self):
        item = create(Builder('dx item').titled(u'Foo'))
        partial = getMultiAdapter((item, None), IPartial, name="fields")
        self.assertDictContainsSubset(
            {u'title': u'Foo'},
            partial(config={'field_dottednames': False}))
