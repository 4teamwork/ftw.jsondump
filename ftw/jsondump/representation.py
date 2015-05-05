from ftw.jsondump.interfaces import IJSONRepresentation
from ftw.jsondump.interfaces import IPartial
from zope.component import adapts
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
import json


class JSONRepresentation(object):
    implements(IJSONRepresentation)
    adapts(Interface, Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def json(self, only=None, **config):
        if only:
            partials = self.get_selected_partials(only)

        else:
            partials = getAdapters((self.context, self.request), IPartial)

        data = {}
        for name, partial in partials:
            data.update(partial(config))
        return json.dumps(data, sort_keys=True, indent=4)

    def get_selected_partials(self, names):
        for name in names:
            yield name, getMultiAdapter((self.context, self.request), IPartial, name=name)
