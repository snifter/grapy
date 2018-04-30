from os import path, remove
from random import randint
from tempfile import TemporaryDirectory
from unittest import TestCase

from grapy.store.node import NODE_STORE_FILE_NAME, NodeStore, NodeRecord


class NodeStoreTestCase(TestCase):

    temp_dir = None

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls.temp_dir.cleanup()

    def tearDown(self):
        file_name = path.join(self.temp_dir.name, NODE_STORE_FILE_NAME)
        if path.exists(file_name):
            remove(file_name)

    def test_write_to_file(self):
        records = 10

        with NodeStore(dir=self.temp_dir.name) as store:
            record_size = store.record_size

            for i in range(records):
                record = NodeRecord(1, i, i, i, i, i, i)
                store.write(record)

        file_name = path.join(self.temp_dir.name, NODE_STORE_FILE_NAME)

        self.assertTrue(path.exists(file_name), 'File has been created')

        expected = record_size * records
        actual = path.getsize(file_name)

        self.assertEqual(expected, actual, 'File has expected size')

    def test_read_record(self):
        records = []

        # create store file
        with NodeStore(dir=self.temp_dir.name) as store:
            for i in range(10):
                record = NodeRecord(i % 2,
                                    randint(0, 9),
                                    randint(0, 9),
                                    randint(0, 9),
                                    randint(0, 9),
                                    randint(0, 9),
                                    randint(0, 9))
                record_id = store.write(record)

                records.append((record_id, list(record)))

        # test
        with NodeStore(dir=self.temp_dir.name) as store:
            for i in [9, 5, 2]:
                record_id = records[i][0]
                record_values = records[i][1]

                record = store.read(record_id)

                self.assertListEqual(record_values, list(record), 'Record is properly read from file')
