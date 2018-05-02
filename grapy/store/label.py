from os import path, SEEK_END
from struct import Struct
from threading import Lock

LABEL_RECORD_FORMAT = '<20s'
# little-endian
# 20 bytes - name - char[]

LABEL_STORE_FILE_NAME = 'grapy.labels.db'


class LabelRecord:
    def __init__(self, value):
        if isinstance(value, str):
            raw = bytes(value, 'ascii')
        else:
            raw = value

        if len(raw) > 20:
            raise ValueError('Value of record can be at most 20 bytes')

        self.value = raw.ljust(20)

    @staticmethod
    def _make(args):
        return LabelRecord(*args)

    @property
    def name(self):
        name = self.value.decode('ascii')
        return name.strip()

    def __iter__(self):
        return iter([self.value])


class LabelStore:
    def __init__(self, dir='.'):
        self.__struct = Struct(LABEL_RECORD_FORMAT)
        self.__file = None
        self.__dir = dir
        self.__lock = Lock()

    @property
    def record_size(self):
        return self.__struct.size

    @property
    def store_file(self):
        return path.join(self.__dir, LABEL_STORE_FILE_NAME)

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
            record = LabelRecord._make(self.__struct.unpack(buffer))

        return record
