from unittest import TestCase

from grapy.store.base.descryptor import ConstantLengthBytes

sample_value_length = 20


class Sample:
    value = ConstantLengthBytes(sample_value_length)


class ConstantLengthBytesTestCase(TestCase):
    def setUp(self):
        self.sample = Sample()

    def test_can_be_created_from_string(self):
        name = 'test_name'

        self.sample.value = name

        self.assertEqual(name.encode('ascii'), self.sample.value.strip(), 'Record has expected value')

    def test_can_be_created_from_bytes(self):
        value = b'test_value'
        self.sample.value = value

        self.assertEqual(value, self.sample.value.strip(), 'Record has expected value')

    def test_value_is_padded_on_end(self):
        value = b'test_value'
        self.sample.value = value

        self.assertEqual(sample_value_length, len(self.sample.value), 'Record has expected length')
        self.assertTrue(self.sample.value.startswith(value), 'Padding is added on end')

    def test_raises_if_value_too_long(self):
        value = b'a' * (sample_value_length + 1)

        with self.assertRaises(ValueError):
            self.sample.value = value
