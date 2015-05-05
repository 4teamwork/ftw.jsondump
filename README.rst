``ftw.jsondump`` provides JSON representations for Plone objects.
By using adapters the JSON representation can easily be customized.

.. contents:: Table of Contents


Installation
============

Add the package as dependency to your setup.py:

.. code:: python

  setup(...
        install_requires=[
          ...
          'ftw.jsondump',
        ])

or to your buildout configuration:

.. code:: ini

  [instance]
  eggs += ftw.jsondump

and rerun buildout.


Usage
=====

For extracting the JSON of an object, use the ``IJSONRepresentation`` adapter:

.. code:: python

  from ftw.jsondump.interfaces import IJSONRepresentation
  from zope.component import getMultiAdapter

  json_representation = getMultiAdapter((context, request), IJSONRepresentation)
  print json_representation.json()


Partials
--------

The JSON is built using "partials", which are merged into one ``dict``.

There are various default partials:

- ``metadata`` partial, providing infos such as ``_type`` and ``_class``
- ``fields`` partial extracting Archetypes and Dexterity field data
- ``uid`` partial, providing the UID in ``_uid``
- ``localroles`` partial, extracting the local roles
- ``workflow`` partial, providing the ``_workflow_chain`` and the ``_workflow_history``
- ``properties`` partial, providing local properties in ``_properties``
- ``interfaces`` partial, extracting the directly provided interfaces in ``_directly_provided``

**Selecting partials**

The desired partials can be selected when extracting the JSON:

.. code:: python

  from ftw.jsondump.interfaces import IJSONRepresentation
  from zope.component import getMultiAdapter

  json_representation = getMultiAdapter((context, request), IJSONRepresentation)
  print json_representation.json(only=['fields', 'metadata'])
  print json_representation.json(exclude=['localroles'])


**File blob data**
The file data is extracted by default as base64 encoded string and embedded in the
JSON document.

This fieldata can be excluded with the ``filedata`` configuration:

.. code:: python

  from ftw.jsondump.interfaces import IJSONRepresentation
  from zope.component import getMultiAdapter

  json_representation = getMultiAdapter((context, request), IJSONRepresentation)
  print json_representation.json(filedata=False)

For doing custom things with the filedata, a callback can be used:

.. code:: python

  from ftw.jsondump.interfaces import IJSONRepresentation
  from zope.component import getMultiAdapter

  def file_callback(context, fieldname, data, filename, mimetype, jsondata):
      with open('./tmp/' + filename, 'w+b') as target:
        target.write(data)

  json_representation = getMultiAdapter((context, request), IJSONRepresentation)
  print json_representation.json(file_callback=file_callback)


Creating custom partials
------------------------

Custom partials can easily be registered as adapter:

*configure.zcml:*

.. code:: xml

  <adapter factory=".partial.CustomAnnotations" name="custom_annotations" />


*partial.py:*

.. code:: python

  from ftw.jsondump.interfaces import IPartial
  from my.package.interfaces import ICustomContent
  from zope.annotation import IAnnotations
  from zope.component import adapts
  from zope.interface import Interface
  from zope.interface import implements

  class CustomAnnotations(object):
      implements(IPartial)
      adapts(ICustomContent, Interface)


      def __init__(self, context, request):
          self.context = context
          self.request = request

      def __call__(self, config):
          annotations = IAnnotations(self.context)
          return {'_custom_annotations': dict(annotations.get('custom_config'))}


Field data extractors
---------------------

The Archetypes and Dexterity partial use field data extractor adapters for extracting
the field data and converting it to a JSON serializable value.

Custom extractors can easily be registered for custom fields:

*configure.zcml:*

.. code:: xml

    <adapter factory=".extractor.CustomFieldExtractor" />

*extractor.py:*

.. code:: python

  from ftw.jsondump.interfaces import IFieldExtractor
  from my.package import ICustomField
  from zope.component import adapts
  from zope.interface import implements
  from zope.interface import Interface


  class CustomFieldExtractor(object):
      implements(IFieldExtractor)
      adapts(Interface, Interface, ICustomField)

      def __init__(self, context, request, field):
          self.context = context
          self.request = request
          self.field = field

      def extract(self, name, data, config):
          value = self.field.get(self.context)
          value = value.prepare_for_serialization()
          data.update({name: value})


Links
=====

- Github: https://github.com/4teamwork/ftw.jsondump
- Issues: https://github.com/4teamwork/ftw.jsondump/issues
- Pypi: http://pypi.python.org/pypi/ftw.jsondump
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.jsondump

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.jsondump`` is licensed under GNU General Public License, version 2.
