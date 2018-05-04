class RecordValidation(type):
    def __new__(mcs, name, bases, class_dict):
        if bases != (object,):
            if '__iter__' not in class_dict:
                raise TypeError('Record implementation has to provide __iter__ method')

        return type.__new__(mcs, name, bases, class_dict)


class Record(object, metaclass=RecordValidation):
    pass


class RecordFactory:
    def __init__(self, record_type):
        self.record_type = record_type

    def __call__(self, args):
        return self.record_type(*args)
