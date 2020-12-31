import uuid

from moonleap.utils import str_to_type_id


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
        return str_to_type_id(self.__module__)

    @property
    def vendor(self):
        return self.__module__.split(".")[-2]

    @property
    def module(self):
        return self.__module__.split(".")[-1]

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
        terms = self.block.get_terms(include_parents=False)
        return other_resource.term in terms

    def drop_from_block(self):
        self.block.drop_resource(self)
