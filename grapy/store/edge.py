from grapy.store.base.descryptor import ConstantLengthBytes
from grapy.store.base.record import Record, RecordFactory
from grapy.store.base.store import RecordStore

EDGE_TYPE_RECORD_FORMAT = '<40s'
# little-endian
# 40 bytes - name - char[]

EDGE_TYPE_STORE_FILE_NAME = 'grapy.edgetypes.db'


class EdgeTypeRecord(Record):

    value = ConstantLengthBytes(40)

    def __init__(self, value):
        self.value = value

    @property
    def name(self):
        name = self.value.decode('utf-8')
        return name.strip()

    def __iter__(self):
        return iter([self.value])


class EdgeTypeStore(RecordStore):

    record_format = EDGE_TYPE_RECORD_FORMAT
    store_file_name = EDGE_TYPE_STORE_FILE_NAME
    record_factory = RecordFactory(EdgeTypeRecord)

    def __init__(self, dir='.'):
        super().__init__(dir)
