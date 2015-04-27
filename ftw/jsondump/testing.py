from ftw.builder.testing import BUILDER_LAYER
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from zope.configuration import xmlconfig


class FtwJsondumpLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import z3c.autoinclude
        xmlconfig.file('meta.zcml', z3c.autoinclude,
                       context=configurationContext)
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <includePlugins package="plone" />'
            '</configure>',
            context=configurationContext)

        import ftw.jsondump
        xmlconfig.file('configure.zcml', ftw.jsondump,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_JSONDUMP_FIXTURE = FtwJsondumpLayer()
FTW_JSONDUMP_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_JSONDUMP_FIXTURE,), name="FtwJsondump:Integration")
