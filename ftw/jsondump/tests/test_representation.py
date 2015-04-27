from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getMultiAdapter
import json


class TestJSONRepresentation(TestCase):

    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def setUp(self):
        ref_document1 = create(Builder('document')
                               .titled("Ref 1"))
        ref_document2 = create(Builder('document')
                               .titled("Ref 2"))

        file_data = 'File data'
        file_ = StringIO(file_data)
        file_.filename = 'test.doc'

        image_data = (
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')
        image_ = StringIO(image_data)
        image_.filename = 'test.gif'

        self.document = create(Builder('document')
                               .titled("My document")
                               .having(text='<p>"S\xc3\xb6mesimple" <b>markup</b></p>',
                                       effectiveDate=DateTime(),
                                       demo_interger_field=42,
                                       demo_float_field=42.0,
                                       demo_fixedpoint_field="42.00",
                                       relatedItems=[
                                           ref_document1, ref_document2],
                                       demo_file_blob_field=file_,
                                       demo_image_blob_field=image_))

    def test_data_is_json_serializable(self):
        adapter = getMultiAdapter((self.document, self.document.REQUEST),
                                  IJSONRepresentation)

        json_data = adapter.json()
        self.assertTrue(isinstance(json.loads(json_data), dict))
