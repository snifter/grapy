from collections import namedtuple
from enum import IntEnum
from struct import Struct

from grapy.store.base.descryptor import ConstantLengthBytes
from grapy.store.base.record import Record, RecordFactory
from grapy.store.base.store import RecordStore


PROPERTY_NAME_RECORD_FORMAT = '<40s'
# little-endian
# 40 bytes - name - char[]

PROPERTY_HEADER_RECORD_FORMAT = '<QQHQ'
# little-endian
# property name pointer (integer)
# next property pointer (integer)
# property type (integer)
# property length (integer)
# property value is saved after header

PROPERTY_NAME_STORE_FILE_NAME = 'grapy.propertynames.db'
PROPERTY_STORE_FILE_NAME = 'grapy.properties.db'


PropertyHeader = namedtuple('PropertyHeader', 'name_pointer next_property type length')


class PropertyRecord(Record):
    def __init__(self, header):
        self.header = header
        self.value = None

    def __iter__(self):
        collection = list(self.header)
        collection.append(self.value)

        return iter(collection)


class PropertyType(IntEnum):
    INTEGER = 1
    FLOAT = 2
    BOOL = 3
    BYTES = 4
    STRING = 5


class RecordType:
    def __init__(self, record):
        self.__record = record

    @property
    def type(self):
        value = self.__record.value
        if isinstance(value, bool):
            return PropertyType.BOOL
        elif isinstance(value, int):
            return PropertyType.INTEGER
        elif isinstance(value, float):
            return PropertyType.FLOAT
        elif isinstance(value, (bytearray, bytes)):
            return PropertyType.BYTES
        elif isinstance(value, str):
            return PropertyType.STRING
        else:
            raise ValueError('Type {0} is not supported as property value type'.format(type(value)))


class ValueStructFormatFactory:
    def for_store(self, serialized_value):
        if isinstance(serialized_value, bool):
            return '<?'
        elif isinstance(serialized_value, int):
            return '<q'
        elif isinstance(serialized_value, float):
            return '<d'
        elif isinstance(serialized_value, (bytearray, bytes)):
            return '<{0}s'.format(len(serialized_value))
        else:
            raise ValueError('Type {0} is not supported as property value type'.format(type(serialized_value)))

    def for_restore(self, header):
        property_type = header.type
        length = header.length

        if property_type == PropertyType.BOOL:
            return '<?'
        elif property_type == PropertyType.INTEGER:
            return '<q'
        elif property_type == PropertyType.FLOAT:
            return '<d'
        elif property_type in [PropertyType.BYTES, PropertyType.STRING]:
            return '<{0}s'.format(length)


class ValueSerializer:
    def __init__(self, record):
        self.__record = record

    def serialize(self):
        value = self.__record.value

        if isinstance(value, str):
            return value.encode('utf-8')

        return self.__record.value


class ValueDeserializer:
    def __init__(self, header):
        self.__header = header

    def deserialize(self, stored_value):
        if self.__header.type == PropertyType.STRING:
            return stored_value.decode('utf-8')

        return stored_value


class PropertyStore(RecordStore):

    record_format = PROPERTY_HEADER_RECORD_FORMAT
    store_file_name = PROPERTY_STORE_FILE_NAME
    record_factory = PropertyHeader._make

    def __init__(self, dir='.'):
        super().__init__(dir)
        self.__value_structs = dict()
        self.__value_struct_factory = ValueStructFormatFactory()

    def _read_record(self, record_id):
        header = super()._read_record(record_id)

        struct_format = self.__value_struct_factory.for_restore(header)
        struct = self.__get_struct(struct_format)

        buffer = self._file.read(header.length)
        stored_value = struct.unpack(buffer)

        value = ValueDeserializer(header).deserialize(stored_value)

        record = PropertyRecord(header)
        record.value = value

        return record

    def _write_record(self, record):
        serializer = ValueSerializer(record)
        serialized_value = serializer.serialize()

        struct_format = self.__value_struct_factory.for_store(serialized_value)
        struct = self.__get_struct(struct_format)

        header = record.header
        header.type = RecordType(record).type
        header.length = struct.size

        record_id = super()._write_record(header)
        self._file.write(struct.pack(serialized_value))

        return record_id

    def __get_struct(self, struct_format):
        struct = self.__value_structs.get(struct_format, None)
        if not struct:
            struct = Struct(struct_format)
            self.__value_structs[struct_format] = struct

        return struct


class PropertyNameRecord(Record):

    value = ConstantLengthBytes(40)

    def __init__(self, value):
        self.value = value

    @property
    def name(self):
        name = self.value.decode('ascii')
        return name.strip()

    def __iter__(self):
        return iter([self.value])


class PropertyNameStore(RecordStore):

    record_format = PROPERTY_NAME_RECORD_FORMAT
    store_file_name = PROPERTY_NAME_STORE_FILE_NAME
    record_factory = RecordFactory(PropertyNameRecord)

    def __init__(self, dir='.'):
        super().__init__(dir)
