from xml.etree import ElementTree

RDF_NAMESPACE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
SCHEMA_NAMESPACE = 'https://schema.org/'

ElementTree.register_namespace('rdf', RDF_NAMESPACE)
ElementTree.register_namespace('schema', SCHEMA_NAMESPACE)

RESOURCE_PROPERTIES = {
    'acquireLicensePage',
    'availability',
    'contentUrl',
    'eventAttendanceMode',
    'eventStatus',
    'license',
    'sameAs',
    'subjectOf',
    'url',
}


def _qualified(namespace, name):
    return f'{{{namespace}}}{name}'


def _append_value(parent, key, value):
    if value is None:
        return
    if isinstance(value, list):
        for item in value:
            _append_value(parent, key, item)
        return

    property_element = ElementTree.SubElement(parent, _qualified(SCHEMA_NAMESPACE, key))
    if isinstance(value, dict):
        node_type = value.get('@type', 'Thing')
        attributes = {}
        if value.get('@id'):
            attributes[_qualified(RDF_NAMESPACE, 'about')] = value['@id']
        node = ElementTree.SubElement(
            property_element,
            _qualified(SCHEMA_NAMESPACE, node_type),
            attributes,
        )
        for nested_key, nested_value in value.items():
            if not nested_key.startswith('@'):
                _append_value(node, nested_key, nested_value)
        return

    if (
        key in RESOURCE_PROPERTIES
        and isinstance(value, str)
        and value.startswith(('http://', 'https://'))
    ):
        property_element.set(_qualified(RDF_NAMESPACE, 'resource'), value)
    elif isinstance(value, bool):
        property_element.text = str(value).lower()
    else:
        property_element.text = str(value)


def render_event_rdf(schema):
    root = ElementTree.Element(_qualified(RDF_NAMESPACE, 'RDF'))
    event = ElementTree.SubElement(
        root,
        _qualified(SCHEMA_NAMESPACE, schema.get('@type', 'Event')),
        {_qualified(RDF_NAMESPACE, 'about'): schema['@id']},
    )
    for key, value in schema.items():
        if not key.startswith('@'):
            _append_value(event, key, value)
    return ElementTree.tostring(root, encoding='utf-8', xml_declaration=True)
