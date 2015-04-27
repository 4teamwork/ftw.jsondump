from base64 import b64encode
from ftw.jsondump.interfaces import IFieldExtractor
from Products.Archetypes.interfaces.field import IFileField
from Products.Archetypes.interfaces.field import IImageField
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class FileFieldExtractor(object):
    implements(IFieldExtractor)
    adapts(Interface, Interface, IFileField)

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def extract(self, name, data, config):
        value = self.field.get(self.context)
        mimetype = self.field.getContentType(self.context)
        data.update({'{0}:file'.format(name): b64encode(value.data),
                     '{0}:mimetype'.format(name): mimetype,
                     '{0}:size'.format(name): len(value.data),
                     '{0}:filename'.format(name): value.filename})


class ImageFieldExtractor(FileFieldExtractor):
    adapts(Interface, Interface, IImageField)
