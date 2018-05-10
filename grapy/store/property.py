from collections import namedtuple
from enum import IntEnum

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


class PropertyType(IntEnum):
    INTEGER = 1
    FLOAT = 2
    BOOL = 3
    BYTES = 4


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
