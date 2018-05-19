from os import path, remove
from random import randint, random
from tempfile import TemporaryDirectory
from unittest import TestCase

from grapy.store.property import PropertyNameRecord, PropertyRecord, PropertyType, RecordType, ValueSerializer, \
    PropertyHeader, ValueDeserializer, ValueStructFormatFactory, PROPERTY_STORE_FILE_NAME, PropertyStore


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


def integer_value_factory():
    return randint(0, 1000)


def float_value_factory():
    return random()


def bool_value_factory():
    return randint(0, 1) == 1


def bytes_value_factory():
    size = randint(10, 255)
    return bytes([randint(0, 255) for _ in range(size)])


def string_value_factory():
    return str(random())


class PropertyStoreTestCase(TestCase):
    temp_dir = None

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def tearDown(self):
        file_name = path.join(self.temp_dir.name, PROPERTY_STORE_FILE_NAME)
        if path.exists(file_name):
            remove(file_name)

    def test_store_file_is_created(self):
        header = PropertyHeader(0, 0, 0, 0)
        record = PropertyRecord(header)
        record.value = 1

        with PropertyStore(dir=self.temp_dir.name) as store:
            store.write(record)

        file_name = path.join(self.temp_dir.name, PROPERTY_STORE_FILE_NAME)

        self.assertTrue(path.exists(file_name), 'File has been created')

    def test_integer_write_read(self):
        self.__test_write_read(integer_value_factory)

    def test_float_write_read(self):
        self.__test_write_read(float_value_factory)

    def test_bool_write_read(self):
        self.__test_write_read(bool_value_factory)

    def test_bytes_write_read(self):
        self.__test_write_read(bytes_value_factory)

    def test_string_write_read(self):
        self.__test_write_read(string_value_factory)

    def test_monkey_mode_write_read(self):
        factories = [
            integer_value_factory,
            float_value_factory,
            bool_value_factory,
            bytes_value_factory,
            string_value_factory
        ]

        def value_factory():
            factory = factories[randint(0, len(factories) - 1)]
            return factory()

        self.__test_write_read(value_factory, 1000)

    def __test_write_read(self, value_factory, iterations=10):
        records = []

        # write
        with PropertyStore(dir=self.temp_dir.name) as store:
            for i in range(iterations):
                header = PropertyHeader(0, 0, 0, 0)
                record = PropertyRecord(header)
                record.value = value_factory()

                record_id = store.write(record)

                records.append((record_id, list(record)))

        # read
        with PropertyStore(dir=self.temp_dir.name) as store:
            for record_id, record_values in records:
                record = store.read(record_id)

                self.assertListEqual(record_values, list(record), 'Record is properly read from file')


class PropertyNameRecordTestCase(TestCase):
    def test_can_be_created_from_string(self):
        name = 'test_name_ążźćś'

        record = PropertyNameRecord(name)

        self.assertEqual(name, record.name, 'Record has expected name')
        self.assertEqual(name.encode('utf-8'), record.value.strip(), 'Record has expected value')

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
