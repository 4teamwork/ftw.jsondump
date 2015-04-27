from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import IReferenceField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface
from plone.uuid.interfaces import IUUID


class ReferenceFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IReferenceField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):

        references = self.field.get(self.context)

        key_path = '{0}:path'.format(name)
        value_path = map(lambda item: '/'.join(item.getPhysicalPath()),
                         references)

        key_uuid = '{0}:uuid'.format(name)
        value_uuid = map(lambda item: IUUID(item), references)
        data.update({key_path: value_path,
                     key_uuid: value_uuid})
