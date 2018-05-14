from unittest import TestCase

from grapy.store.property import PropertyNameRecord, PropertyRecord, PropertyType, RecordType, ValueSerializer, \
    PropertyHeader, ValueDeserializer, ValueStructFormatFactory


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


class ValueSerializerTestCase(TestCase):
    def test_base_types_not_changed(self):
        values = [
            3,
            3.3,
            True, False,
            b'test_bytes'
        ]
        for value in values:
            record = PropertyRecord(None)
            record.value = value
            target = ValueSerializer(record)

            self.assertEqual(value, target.serialize(), 'Serialized value should be not changed')

    def test_string_serialized_as_bytes(self):
        value = 'test string'

        record = PropertyRecord(None)
        record.value = value
        target = ValueSerializer(record)

        expected = value.encode('utf-8')
        actual = target.serialize()

        self.assertEqual(expected, actual, 'string should be converted to bytes')


class ValueDeserializerTestCase(TestCase):
    def test_base_types_not_changed(self):
        values = [
            (PropertyType.INTEGER, 3),
            (PropertyType.FLOAT, 3.3),
            (PropertyType.BOOL, True),
            (PropertyType.BOOL, False),
            (PropertyType.BYTES, b'test_bytes')
        ]
        for property_type, value in values:
            header = PropertyHeader(0, 0, property_type, 0)
            target = ValueDeserializer(header)

            actual = target.deserialize(value)

            self.assertEqual(value, actual, 'value is not changed')

    def test_strings_is_deserialized_from_bytes(self):
        value = b'test bytes'

        header = PropertyHeader(0, 0, PropertyType.STRING, 0)
        target = ValueDeserializer(header)

        expected = value.decode('utf-8')
        actual = target.deserialize(value)

        self.assertEqual(expected, actual, 'string should be restored from bytes')


class ValueStructFormatFactoryTestCase(TestCase):
    def test_for_store(self):
        data = [
            (3, '<q'),
            (-3, '<q'),
            (3.3, '<d'),
            (-3.3, '<d'),
            (True, '<?'),
            (False, '<?'),
            (b'test_bytes', '<10s')
        ]

        target = ValueStructFormatFactory()
        for value, expected in data:
            actual = target.for_store(value)
            self.assertEqual(expected, actual, 'Should be valid format')

    def test_for_restore(self):
        data = [
            (PropertyType.INTEGER, 0, '<q'),
            (PropertyType.INTEGER, 0, '<q'),
            (PropertyType.FLOAT, 0, '<d'),
            (PropertyType.FLOAT, 0, '<d'),
            (PropertyType.BOOL, 0, '<?'),
            (PropertyType.BOOL, 0, '<?'),
            (PropertyType.BYTES, 13, '<13s'),
            (PropertyType.STRING, 14, '<14s')
        ]

        target = ValueStructFormatFactory()
        for property_type, length, expected in data:
            header = PropertyHeader(0, 0, property_type, length)
            actual = target.for_restore(header)
            self.assertEqual(expected, actual, 'Should be valid format')


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
