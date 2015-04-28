from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
from zope.component import getMultiAdapter
import json


class TestMetadataPartial(TestCase):
    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def test_metadata_partial(self):
        folder = create(Builder('folder'))
        create(Builder('document').within(folder))
        document = create(Builder('document').within(folder))

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="metadata")
        data = partial({})

        self.assertEquals(
            {'_classname': 'ATDocument',
             '_class': 'Products.ATContentTypes.content.document.ATDocument',
             '_id': 'document-1',
             '_obj_position_in_parent': 1,  # object position in parent
             '_owner': TEST_USER_ID,
             '_path': '/plone/folder/document-1',
             '_type': 'Document'},
            data)

        self.assertEquals(json.loads(json.dumps(data)), data)
