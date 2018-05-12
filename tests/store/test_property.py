from unittest import TestCase

from grapy.store.property import PropertyNameRecord, PropertyRecord, PropertyType, RecordType


class PropertyTypeTestCase(TestCase):
    def setUp(self):
        self.record = PropertyRecord(None)

    def test_integer_type(self):
        self.record.value = 3
        target = RecordType(self.record)
        self.assertEqual(PropertyType.INTEGER, target.type, 'for number type is set to INTEGER')

    def test_float_type(self):
        self.record.value = 3.3
        target = RecordType(self.record)
        self.assertEqual(PropertyType.FLOAT, target.type, 'for decimal number type is set to FLOAT')

    def test_bool_type(self):
        self.record.value = True
        target = RecordType(self.record)
        self.assertEqual(PropertyType.BOOL, target.type, 'for True type is set to BOOL')

        self.record.value = False
        target = RecordType(self.record)
        self.assertEqual(PropertyType.BOOL, target.type, 'for False type is set to BOOL')

    def test_bytes_type(self):
        self.record.value = b'test'
        target = RecordType(self.record)
        self.assertEqual(PropertyType.BYTES, target.type, 'for bytes type is set to BYTES')

        self.record.value = bytearray('test', 'utf-8')
        target = RecordType(self.record)
        self.assertEqual(PropertyType.BYTES, target.type, 'for bytes type is set to BYTES')

    def test_string_type(self):
        self.record.value = 'another test'
        target = RecordType(self.record)
        self.assertEqual(PropertyType.STRING, target.type, 'for string type is set to STRING')


class PropertyNameRecordTestCase(TestCase):
    def test_can_be_created_from_string(self):
        name = 'test_name'

        record = PropertyNameRecord(name)

        self.assertEqual(name, record.name, 'Record has expected name')
        self.assertEqual(name.encode('ascii'), record.value.strip(), 'Record has expected value')

    def test_can_be_created_from_bytes(self):
        value = b'test_value'

        record = PropertyNameRecord(value)

        self.assertEqual(value, record.value.strip(), 'Record has expected value')
        self.assertEqual(value.decode(), record.name, 'Record has expected name')

    def test_is_iterable(self):
        name = 'test_name'

        record = PropertyNameRecord(name)

        as_list = list(record)
        self.assertEqual(1, len(as_list), 'List has one item')
        self.assertEqual(record.value, as_list[0], 'Item has expected value')
