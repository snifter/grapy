from collections import namedtuple

from grapy.store.base.descryptor import ConstantLengthBytes
from grapy.store.base.record import Record, RecordFactory
from grapy.store.base.store import RecordStore

EDGE_TYPE_RECORD_FORMAT = '<40s'
# little-endian
# 40 bytes - name - char[]

EDGE_RECORD_FORMAT = '<?QQQQI'
# little-endian
# 1 byte - in use - deleted or not (bool)
# 8 bytes - first node pointer (integer)
# 8 bytes - second node pointer (integer)
# 8 bytes - next edge pointer (integer)
# 8 bytes - first property pointer (integer)
# 4 bytes - edge type pointers (integer)

EDGE_TYPE_STORE_FILE_NAME = 'grapy.edgetypes.db'

EDGE_STORE_FILE_NAME = 'grapy.edges.db'

EdgeRecord = namedtuple('EdgeRecord', 'in_use first_node second_node next_edge first_property edge_type')


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


class EdgeStore(RecordStore):

    record_format = EDGE_RECORD_FORMAT
    store_file_name = EDGE_STORE_FILE_NAME
    record_factory = EdgeRecord._make

    def __init__(self, dir='.'):
        super().__init__(dir)


class EdgeTypeStore(RecordStore):

    record_format = EDGE_TYPE_RECORD_FORMAT
    store_file_name = EDGE_TYPE_STORE_FILE_NAME
    record_factory = RecordFactory(EdgeTypeRecord)

    def __init__(self, dir='.'):
        super().__init__(dir)
