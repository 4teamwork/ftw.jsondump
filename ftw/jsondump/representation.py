from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.interfaces import IPartial
from zope.component import adapts
from zope.component import getAdapters
from zope.interface import implements
from zope.interface import Interface
import json


class JSONRepresentation(object):
    implements(IJSONRepresentation)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def json(self, **config):
        data = {}

        for name, partial in getAdapters((self.context, self.request), IPartial):
            data.update(partial(config))

        return json.dumps(data)
