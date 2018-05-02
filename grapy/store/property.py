
class PropertyNameRecord:
    def __init__(self, value):
        if isinstance(value, str):
            raw = bytes(value, 'ascii')
        else:
            raw = value

        if len(raw) > 40:
            raise ValueError('Value of record can be at most 40 bytes')

        self.value = raw.ljust(40)

    @property
    def name(self):
        name = self.value.decode('ascii')
        return name.strip()

    def __iter__(self):
        return iter([self.value])
