from os import path, remove
from random import randint
from tempfile import TemporaryDirectory
from unittest import TestCase

from grapy.store.label import LABEL_STORE_FILE_NAME, LabelStore, LabelRecord, LabelRecordFactory


class LabelRecordFactoryTestCase(TestCase):
    def test_create_instance_from_tuple(self):
        label = b'test_label'

        factory = LabelRecordFactory()
        record = factory((label,))

        self.assertEqual(label.decode(), record.name, 'Record has expected name')


class LabelRecordTestCase(TestCase):
    def test_can_be_created_from_string(self):
        name = 'test_label'

        record = LabelRecord(name)

        self.assertEqual(name, record.name, 'Record has expected name')
        self.assertEqual(name.encode('ascii'), record.value.strip(), 'Record has expected value')

    def test_can_be_created_from_bytes(self):
        value = b'test_label'

        record = LabelRecord(value)

        self.assertEqual(value, record.value.strip(), 'Record has expected value')
        self.assertEqual(value.decode(), record.name, 'Record has expected name')

    def test_is_iterable(self):
        name = 'test_label'

        record = LabelRecord(name)

        as_list = list(record)
        self.assertEqual(1, len(as_list), 'List has one item')
        self.assertEqual(record.value, as_list[0], 'Item has expected value')


class LabelStoreTestCase(TestCase):

    temp_dir = None

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def tearDown(self):
        file_name = path.join(self.temp_dir.name, LABEL_STORE_FILE_NAME)
        if path.exists(file_name):
            remove(file_name)

    def test_write_to_file(self):
        records = 10

        with LabelStore(dir=self.temp_dir.name) as store:
            record_size = store.record_size

            for i in range(records):
                record = LabelRecord('label_{0}'.format(i))
                store.write(record)

        file_name = path.join(self.temp_dir.name, LABEL_STORE_FILE_NAME)

        self.assertTrue(path.exists(file_name), 'File has been created')

        expected = record_size * records
        actual = path.getsize(file_name)

        self.assertEqual(expected, actual, 'File has expected size')

    def test_read_record(self):
        records = []

        # create store file
        with LabelStore(dir=self.temp_dir.name) as store:
            for i in range(10):
                record = LabelRecord('label_{}'.format(randint(0, 100)))
                record_id = store.write(record)

                records.append((record_id, list(record)))

        # test
        with LabelStore(dir=self.temp_dir.name) as store:
            for i in [9, 5, 2]:
                record_id = records[i][0]
                record_values = records[i][1]

                record = store.read(record_id)

                self.assertListEqual(record_values, list(record), 'Record is properly read from file')
