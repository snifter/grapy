from unittest import TestCase

from grapy.store.edge import EdgeTypeRecord
from tests.store.common.record import NamedRecordTestCaseMixin


class EdgeTypeRecordTestCase(TestCase, NamedRecordTestCaseMixin):
    record_type = EdgeTypeRecord
