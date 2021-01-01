import uuid

from moonleap.parser.term import Term
from moonleap.utils import resource_id_from_class


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.block = None
        self.term = None

    def __str__(self):
        return self.__class__.__name__

    def describe(self):
        return str(self)

    @property
    def type_id(self):
        return resource_id_from_class(self.__class__)

    @property
    def vendor(self):
        return self.type_id.split(".")[0]

    @property
    def module(self):
        return self.type_id.split(".")[1]

    def is_mentioned_in_same_line(self, other_resource, is_ordered=True):
        for line in self.block.lines:
            if self.term in line.terms and other_resource.term in line.terms:
                return (
                    line.terms.index(self.term) < line.terms.index(other_resource.term)
                    if is_ordered
                    else True
                )

        return False

    def is_created_in_block_that_mentions(self, other_resource):
        return other_resource.term in self.block.get_terms()

    def drop_from_block(self):
        self.block.drop_resource(self)


class Always(Resource):
    def __init__(self):
        self.term = Term("always", "always")
