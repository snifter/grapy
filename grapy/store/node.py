from collections import namedtuple

from grapy.store.base.store import RecordStore

NODE_RECORD_FORMAT = '<?QQ4I'
# little-endian
# 1 byte - in use - deleted or not (bool)
# 8 bytes - first edge pointer (integer)
# 8 bytes - first property pointer (integer)
# 4 * 4 bytes - labels pointers (integer)

NODE_STORE_FILE_NAME = 'grapy.nodes.db'

NodeRecord = namedtuple('NodeRecord', 'in_use first_edge first_property label_1 label_2 label_3 label_4')


class NodeStore(RecordStore):

    record_format = NODE_RECORD_FORMAT
    store_file_name = NODE_STORE_FILE_NAME
    record_factory = NodeRecord._make

    def __init__(self, dir='.'):
        super().__init__(dir)
