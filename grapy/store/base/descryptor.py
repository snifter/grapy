from weakref import WeakKeyDictionary


class ConstantLengthBytes:
    def __init__(self, length):
        self.length = length
        self._values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        return self._values.get(instance, None)

    def __set__(self, instance, value):
        if isinstance(value, str):
            raw = bytes(value, 'utf-8')
        else:
            raw = value

        if len(raw) > self.length:
            raise ValueError('Value can be at most {0} bytes length'.format(self.length))

        self._values[instance] = raw.ljust(self.length)
