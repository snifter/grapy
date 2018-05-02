from grapy.store.base.descryptor import ConstantLengthBytes
from grapy.store.base.record import Record
from grapy.store.base.store import RecordStore

LABEL_RECORD_FORMAT = '<20s'
# little-endian
# 20 bytes - name - char[]

LABEL_STORE_FILE_NAME = 'grapy.labels.db'


class LabelRecordFactory:
    def __call__(self, args):
        return LabelRecord(*args)


class LabelRecord(Record):

    value = ConstantLengthBytes(20)

    def __init__(self, value):
        self.value = value

    @property
    def name(self):
        name = self.value.decode('ascii')
        return name.strip()

    def __iter__(self):
        return iter([self.value])


class LabelStore(RecordStore):

    record_format = LABEL_RECORD_FORMAT
    store_file_name = LABEL_STORE_FILE_NAME
    record_factory = LabelRecordFactory()

    def __init__(self, dir='.'):
        super().__init__(dir)
