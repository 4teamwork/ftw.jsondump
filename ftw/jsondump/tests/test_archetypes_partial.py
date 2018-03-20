from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.testing import IS_PLONE_5
from unittest2 import skipIf
from zope.component import getMultiAdapter
import json


@skipIf(IS_PLONE_5, 'We should refrain from using archetypes from Plone 5 onwards.')
class TestArchetypePartial(FtwJsondumpTestCase):

    def setUp(self):
        self.document = create(Builder('document')
                               .titled(u"My document"))

    def test_partial_is_jsonseriazable(self):
        partial = getMultiAdapter((self.document, self.document.REQUEST),
                                  IPartial,
                                  name="fields")

        config = {}
        partial_data = partial(config)
        self.assertEquals(json.loads(json.dumps(partial_data)), partial_data)
