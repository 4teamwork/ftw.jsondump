from ftw.builder import Builder
from ftw.builder import create
from ftw.jsondump.interfaces import IPartial
from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.component import getMultiAdapter
import json


class TestLocalRolesPartial(TestCase):

    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def setUp(self):
        self.folder = create(Builder('folder'))
        self.user = create(Builder('user')
                           .with_roles('Editor', 'Reader', on=self.folder))

    def test_partial_is_jsonseriazable(self):
        partial = getMultiAdapter((self.folder, self.folder.REQUEST),
                                  IPartial,
                                  name="localroles")

        config = {}
        partial_data = partial(config)
        self.assertEquals({'__ac_local_roles__':
                           {'test_user_1_': ['Owner'],
                            'john.doe': ['Editor', 'Reader']}},
                          partial_data)

        self.assertEquals(json.loads(json.dumps(partial_data)), partial_data)
