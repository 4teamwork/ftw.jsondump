from ftw.jsondump.dexterity.base import PlainFieldExtractor
from plone.app.textfield.value import RichTextValue


class RichTextExtractor(PlainFieldExtractor):

    def extract(self, name, data, config):
        key = self.key(config)
        storage = self.field.interface(self.context)
        value = getattr(storage, name)
        if isinstance(value, RichTextValue):
            data.update({key: value.raw,
                         key + ':mimeType': value.mimeType,
                         key + ':outputMimeType': value.outputMimeType,
                         key + ':encoding': value.encoding})
        else:
            data[key] = value
