import uuid

from moonleap.utils import str_to_type_id


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex

    def __str__(self):
        return self.__class__.__name__

    def describe(self):
        return str(self)

    @property
    def type_id(self):
        return str_to_type_id(self.__module__)

    @property
    def vendor(self):
        return self.__module__.split(".")[-2]

    @property
    def module(self):
        return self.__module__.split(".")[-1]
