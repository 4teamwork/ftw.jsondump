from DateTime import DateTime
from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from ftw.jsondump.tests.helpers import asset
from ftw.testing import freeze
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import getMultiAdapter
import json


class TestJSONRepresentation(TestCase):

    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def test_archetypes_document(self):
        file_ = StringIO('File data')
        file_.filename = 'test.doc'

        image_ = StringIO(asset('empty.gif').bytes())
        image_.filename = 'test.gif'

        with freeze(datetime(2010, 12, 28, 10, 55, 12)):
            document = create(
                Builder('document')
                .titled("My document")
                .having(text='<p>"S\xc3\xb6mesimple" <b>markup</b></p>',
                        effectiveDate=DateTime(),
                        demo_interger_field=42,
                        demo_float_field=42.0,
                        demo_fixedpoint_field="42.00",
                        relatedItems=[create(Builder('document').titled("Ref 1")),
                                      create(Builder('document').titled("Ref 2"))],
                        demo_file_blob_field=file_,
                        demo_image_blob_field=image_))

        adapter = getMultiAdapter((document, document.REQUEST), IJSONRepresentation)
        data = json.loads(adapter.json())
        data['relatedItems:uuid'] = ['<REPLACED>' for uid in data['relatedItems:uuid']]

        expected = json.loads(asset('archetypes_document.json').text())
        self.assert_structure_equal(expected, data)

    def assert_structure_equal(self, expected, got, msg=None):
        got = json.dumps(got, sort_keys=True, indent=4)
        expected = json.dumps(expected, sort_keys=True, indent=4)
        self.maxDiff = None
        self.assertMultiLineEqual(got, expected, msg)
