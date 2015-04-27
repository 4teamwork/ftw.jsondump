from ftw.jsondump.interfaces import IFieldExtractor
from zope.interface import implements


class BaseFieldExtrator(object):
    implements(IFieldExtractor)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = self.convert(self.field.get(self.context))
        data.update({name: value})

    def convert(self, value):
        return value
