from ftw.jsondump.interfaces import IFieldExtractor
from ftw.jsondump.interfaces import IPartial
from Products.Archetypes.interfaces import IBaseObject
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface


class ArchetypFieldsPartial(object):
    implements(IPartial)
    adapts(IBaseObject, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):

        data = {}

        for name, field in self.context.Schema().items():
            getMultiAdapter((self.context, self.request, field),
                            IFieldExtractor).extract(name, data, config)

        return data
