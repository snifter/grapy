from grapy.store.base.descryptor import ConstantLengthBytes
from grapy.store.base.record import Record


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
