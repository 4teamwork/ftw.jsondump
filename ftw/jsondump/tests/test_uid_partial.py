from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.component import getMultiAdapter
import json


class TestUIDPartial(TestCase):
    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def test_uuid_partial(self):
        document = create(Builder('document'))

        partial = getMultiAdapter((document, document.REQUEST), IPartial,
                                  name="uid")
        data = partial({})
        self.assertEquals({'_uid': document.UID()}, data)
        self.assertEquals(json.loads(json.dumps(data)), data)
