from os import path, SEEK_END
from struct import Struct
from threading import Lock


class RecordStoreValidation(type):
    def __new__(mcs, name, bases, class_dict):
        if bases != (object,):
            if 'record_format' not in class_dict:
                raise TypeError('Store implementation has to provide record_format')

            if not isinstance(class_dict['record_format'], str):
                raise ValueError('record_format has to be string')

            if 'store_file_name' not in class_dict:
                raise TypeError('Store implementation has to provide store_file_name')

            if not isinstance(class_dict['store_file_name'], str):
                raise ValueError('store_file_name has to be string')

            if 'record_factory' not in class_dict:
                raise TypeError('Store implementation has to provide record_factory')

            if not callable(class_dict['record_factory']):
                raise ValueError('record_factory has to be callable')

        return type.__new__(mcs, name, bases, class_dict)


class RecordStore(object, metaclass=RecordStoreValidation):

    record_format = None
    store_file_name = None
    record_factory = None

    def __init__(self, dir='.'):
        self.__struct = Struct(self.record_format)
        self._file = None
        self.__dir = dir
        self.__lock = Lock()

    @property
    def record_size(self):
        return self.__struct.size

    @property
    def store_file(self):
        return path.join(self.__dir, self.store_file_name)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self._file = open(self.store_file, 'ab+')

    def close(self):
        if not self._file:
            return

        self._file.close()

    def write(self, record):
        with self.__lock:
            return self._write_record(record)

    def _write_record(self, record):
        self._file.seek(0, SEEK_END)
        record_id = self._file.tell()

        self._file.write(self.__struct.pack(*list(record)))

        return record_id

    def read(self, record_id):
        with self.__lock:
            return self._read_record(record_id)

    def _read_record(self, record_id):
        self._file.seek(record_id)

        buffer = self._file.read(self.record_size)
        record = self.record_factory(self.__struct.unpack(buffer))

        return record
