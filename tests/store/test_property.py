from unittest import TestCase

from grapy.store.property import PropertyNameRecord


class LabelRecordTestCase(TestCase):
    def test_can_be_created_from_string(self):
        name = 'test_property'

        record = PropertyNameRecord(name)

        self.assertEqual(name, record.name, 'Record has expected name')
        self.assertEqual(name.encode('ascii'), record.value.strip(), 'Record has expected value')

    def test_can_be_created_from_bytes(self):
        value = b'test_property'

        record = PropertyNameRecord(value)

        self.assertEqual(value, record.value.strip(), 'Record has expected value')
        self.assertEqual(value.decode(), record.name, 'Record has expected name')

    def test_value_is_padded_on_end(self):
        value = b'test_property'

        record = PropertyNameRecord(value)
        self.assertEqual(40, len(record.value), 'Record has expected length')
        self.assertTrue(record.value.startswith(value), 'Padding is added on end')

    def test_raises_if_label_too_long(self):
        value = b'a' * 41

        with self.assertRaises(ValueError):
            PropertyNameRecord(value)

    def test_is_iterable(self):
        name = 'test_property'

        record = PropertyNameRecord(name)

        as_list = list(record)
        self.assertEqual(1, len(as_list), 'List has one item')
        self.assertEqual(record.value, as_list[0], 'Item has expected value')