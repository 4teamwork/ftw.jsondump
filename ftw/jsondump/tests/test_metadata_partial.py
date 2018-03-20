from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.testing import IS_PLONE_5
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
import json


class TestMetadataPartial(FtwJsondumpTestCase):

    def test_metadata_partial(self):
        folder = create(Builder('folder'))
        create(Builder('document').within(folder))
        document = create(Builder('document').within(folder))

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="metadata")
        data = partial({})

        expected = {'_classname': 'ATDocument',
             '_class': 'Products.ATContentTypes.content.document.ATDocument',
             '_id': 'document-1',
             '_obj_position_in_parent': 1,  # object position in parent
             '_owner': TEST_USER_ID,
             '_path': '/plone/folder/document-1',
             '_type': 'Document'}

        if IS_PLONE_5:
            expected['_classname'] = 'Document'
            expected['_class'] = 'plone.app.contenttypes.content.Document'

        self.assertEquals(expected, data)

        self.assertEquals(json.loads(json.dumps(data)), data)
