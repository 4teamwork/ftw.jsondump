from ftw.jsondump.testing import FTW_JSONDUMP_INTEGRATION_TESTING
from unittest2 import TestCase


class TestPackageInstalled(TestCase):

    layer = FTW_JSONDUMP_INTEGRATION_TESTING

    def test_true(self):
        self.assertTrue(True)
