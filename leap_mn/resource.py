import uuid

from moonleap.utils import str_to_type_id


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex

    def describe(self, indent=0):
        return " " * indent + str(type(self).__name__)

    @property
    def type_id(self):
        return str_to_type_id(self.__module__)

    @property
    def vendor(self):
        return self.__module__.split(".")[-2]

    @property
    def module(self):
        return self.__module__.split(".")[-1]
