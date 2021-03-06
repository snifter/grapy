class NamedRecordTestCaseMixin:
    def test_can_be_created_from_string(self):
        name = 'test_ążźćę'

        record = self.record_type(name)

        self.assertEqual(name, record.name, 'Record has expected name')
        self.assertEqual(name.encode('utf-8'), record.value.strip(), 'Record has expected value')

    def test_can_be_created_from_bytes(self):
        value = b'test'

        record = self.record_type(value)

        self.assertEqual(value, record.value.strip(), 'Record has expected value')
        self.assertEqual(value.decode(), record.name, 'Record has expected name')

    def test_is_iterable(self):
        name = 'test'

        record = self.record_type(name)

        as_list = list(record)
        self.assertEqual(1, len(as_list), 'List has one item')
        self.assertEqual(record.value, as_list[0], 'Item has expected value')
