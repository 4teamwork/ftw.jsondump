from ftw.builder.dexterity import DexterityBuilder
from ftw.builder import builder_registry


class DXItemBuilder(DexterityBuilder):
    portal_type = 'DXItem'


builder_registry.register('dx item', DXItemBuilder)
