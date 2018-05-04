from unittest import TestCase
from unittest.mock import Mock

from grapy.store.base.record import RecordFactory


class RecordFactoryTestCase(TestCase):
    def test_create_instance_from_tuple(self):
        record_type = Mock()

        label = b'test_label'

        factory = RecordFactory(record_type)
        factory((label,))

        record_type.assert_called_once_with(label)
