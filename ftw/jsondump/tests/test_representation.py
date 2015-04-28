from DateTime import DateTime
from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.tests.base import FtwJsondumpTestCase
from ftw.jsondump.tests.helpers import asset
from ftw.testing import freeze
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from zope.component import getMultiAdapter
import json
import re


class TestJSONRepresentation(FtwJsondumpTestCase):

    def setUp(self):
        self.wftool = getToolByName(self.layer['portal'], 'portal_workflow')
        self.wftool.setChainForPortalTypes(('Document',),
                                           ('simple_publication_workflow',))

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
            self.wftool.doActionFor(document, 'publish')
            self.wftool.doActionFor(document, 'retract')

        adapter = getMultiAdapter(
            (document, document.REQUEST), IJSONRepresentation)
        data = json.loads(adapter.json())
        expected = self.get_asset_json('archetypes_document.json')
        self.assert_structure_equal(expected, data)

    def test_dexterity_item(self):
        item = create(
            Builder('dx item')
            .titled(u'The dexterity item'))

        adapter = getMultiAdapter((item, item.REQUEST), IJSONRepresentation)
        data = json.loads(adapter.json())
        expected = self.get_asset_json('dexterity_item.json')
        self.assert_structure_equal(expected, data)

    def get_asset_json(self, name):
        raw = asset(name).text()

        # replace uids
        for marker, path in re.findall(r'(<<uid:([^>]*)>>)', raw):
            obj = self.layer['app'].restrictedTraverse(path.encode('utf-8'))
            raw = raw.replace(marker, obj.UID())

        return json.loads(raw)
