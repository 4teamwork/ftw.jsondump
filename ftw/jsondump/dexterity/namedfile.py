from base64 import b64encode
from ftw.jsondump.dexterity.base import PlainFieldExtractor


class NamedFileExtractor(PlainFieldExtractor):

    def extract(self, name, data, config):
        storage = self.field.interface(self.context)
        value = getattr(storage, name)

        if config.get('filedata', True):
            data['{0}:file'.format(name)] = b64encode(value.data)

        data['{0}:mimetype'.format(name)] = value.contentType.decode('utf-8')
        data['{0}:size'.format(name)] = value.getSize()
        data['{0}:filename'.format(name)] = value.filename.decode('utf-8')
