from unittest import TestCase

from grapy.store.label import LabelRecord
from tests.store.common.record import NamedRecordTestCaseMixin


class LabelRecordTestCase(TestCase, NamedRecordTestCaseMixin):
    record_type = LabelRecord
