from base64 import b64encode
from ftw.jsondump.dexterity.base import PlainFieldExtractor


class NamedFileExtractor(PlainFieldExtractor):

    def extract(self, name, data, config):
        key = self.key(config)
        storage = self.field.interface(self.context)
        value = getattr(storage, name)
        if not value:
            return

        if config.get('filedata', True):
            data['{0}:file'.format(key)] = b64encode(value.data)

        data['{0}:mimetype'.format(key)] = (
            value.contentType.decode('utf-8'))
        data['{0}:size'.format(key)] = value.getSize()
        data['{0}:filename'.format(key)] = value.filename.decode('utf-8')

        file_callback = config.get('file_callback', None)
        if file_callback:
            file_callback(self.context, key, name,
                          value.data, value.filename, value.contentType,
                          data)
