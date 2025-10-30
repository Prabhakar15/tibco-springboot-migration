import os
from generator.xsd_parser import parse_xsd


def test_parse_sample_xsd(tmp_path):
    xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:element name="SampleRequest">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="customerID" type="xs:string"/>
        <xs:element name="amount" type="xs:decimal"/>
        <xs:element name="term" type="xs:int"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>'''
    p = tmp_path / 'sample.xsd'
    p.write_text(xsd, encoding='utf-8')
    res = parse_xsd(str(p))
    assert 'SampleRequest' in res
    fields = dict(res['SampleRequest'])
    assert fields['customerID'] == 'String'
    assert fields['amount'].endswith('BigDecimal')
    assert fields['term'] == 'Integer'
