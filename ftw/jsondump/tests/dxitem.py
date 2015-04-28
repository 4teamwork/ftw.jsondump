from plone.dexterity.content import Item
from plone.directives.form import Schema
from zope.interface import implements


class IDXItemSchema(Schema):
    pass


class DXItem(Item):
    implements(IDXItemSchema)
