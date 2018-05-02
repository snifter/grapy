from grapy.store.base import RecordStore

LABEL_RECORD_FORMAT = '<20s'
# little-endian
# 20 bytes - name - char[]

LABEL_STORE_FILE_NAME = 'grapy.labels.db'


class LabelRecordFactory:
    def __call__(self, args):
        return LabelRecord(*args)


class LabelRecord:
    def __init__(self, value):
        if isinstance(value, str):
            raw = bytes(value, 'ascii')
        else:
            raw = value

        if len(raw) > 20:
            raise ValueError('Value of record can be at most 20 bytes')

        self.value = raw.ljust(20)

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
