"""Simple XSD parser: extracts top-level element names and child fields (from complexType/sequence).
Maps simple XSD types to Java types.
"""
from xml.etree import ElementTree as ET
from typing import Dict, List, Tuple

XSD_NS = '{http://www.w3.org/2001/XMLSchema}'

JAVA_TYPE_MAP = {
    'string': 'String',
    'int': 'Integer',
    'integer': 'Integer',
    'decimal': 'java.math.BigDecimal',
    'boolean': 'Boolean',
    'date': 'java.time.LocalDate',
}


def parse_xsd(xsd_path: str) -> Dict[str, List[Tuple[str, str]]]:
    """Parse XSD file and return a mapping of elementName -> list of (fieldName, javaType).

    This parser handles common patterns of top-level element with a complexType/sequence.
    It is intentionally simple; for production use consider using lxml or an XJC-based codegen.
    """
    tree = ET.parse(xsd_path)
    root = tree.getroot()

    elements = {}

    # Find all top-level elements
    for elem in root.findall(f"{XSD_NS}element"):
        name = elem.get('name')
        # Look for complexType under element
        fields = []
        complex_type = elem.find(f"{XSD_NS}complexType")
        if complex_type is not None:
            sequence = complex_type.find(f"{XSD_NS}sequence")
            if sequence is not None:
                for child in sequence.findall(f"{XSD_NS}element"):
                    fname = child.get('name')
                    ftype = child.get('type') or ''
                    # ftype may be like 'xs:string' or 'tns:SomeType'
                    if ':' in ftype:
                        _, local = ftype.split(':', 1)
                    else:
                        local = ftype
                    java_type = JAVA_TYPE_MAP.get(local, 'String')
                    fields.append((fname, java_type))
        elements[name] = fields
    return elements
