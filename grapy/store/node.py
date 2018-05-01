from collections import namedtuple
from os import path, SEEK_END
from struct import Struct
from threading import Lock

NODE_RECORD_FORMAT = '<?QQBBBB'
# little-endian
# 1 byte - in use - deleted or not (bool)
# 8 bytes - first relationship pointer (integer)
# 8 bytes - first property pointer (integer)
# 4 * 1 byte - labels pointers (integer)

NODE_STORE_FILE_NAME = 'grapy.nodes.db'

NodeRecord = namedtuple('NodeRecord', 'in_use first_relationship first_property label_1 label_2 label_3 label_4')


class NodeStore:
    def __init__(self, dir='.'):
        self.__struct = Struct(NODE_RECORD_FORMAT)
        self.__file = None
        self.__dir = dir
        self.__lock = Lock()

    @property
    def record_size(self):
        return self.__struct.size

    @property
    def store_file(self):
        return path.join(self.__dir, NODE_STORE_FILE_NAME)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.__file = open(self.store_file, 'ab+')

    def close(self):
        if not self.__file:
            return

        self.__file.close()

    def write(self, record):
        with self.__lock:
            self.__file.seek(0, SEEK_END)
            record_id = self.__file.tell()

            self.__file.write(self.__struct.pack(*list(record)))

        return record_id

    def read(self, record_id):
        with self.__lock:
            self.__file.seek(record_id)

            buffer = self.__file.read(self.record_size)
            record = NodeRecord._make(self.__struct.unpack(buffer))

        return record
