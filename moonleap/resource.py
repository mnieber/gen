import uuid

from moonleap.parser.term import Term, word_to_term


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.block = None
        self.line = None
        self.term = None
        self.children = {}
        self.parents = {}

    def __str__(self):
        return self.__class__.__name__

    def add_child(self, child_resource):
        children = self.children.setdefault(child_resource.key, [])
        if child_resource not in children:
            children.append(child_resource)

        parents = child_resource.parents.setdefault(self.key, [])
        if self not in parents:
            parents.append(self)

    def parent(self, resource_type):
        resource_type_id = get_type_id(resource_type)

        parents = self.parents.get(resource_type_id)
        if not parents:
            return None

        if len(parents) > 1:
            raise Exception(
                f"Expected a single parent of type {resource_type_id} in {self}"
            )

        return parents[0]

    def describe(self):
        return str(self)

    @property
    def type_id(self):
        return resource_id_from_class(self.__class__)

    @property
    def key(self):
        return self.type_id

    @property
    def vendor(self):
        return self.type_id.split(".")[0]

    @property
    def module(self):
        return self.type_id.split(".")[1]

    def is_created_in_block_that_describes(self, other_resource):
        return other_resource.term in self.block.lines[0].terms

    def is_paired_with(self, block, other_resource):
        for line in block.lines:
            state = "find start"
            count_other_resources = 0
            for word in line.words:
                term = word_to_term(word)

                if term and term == self.term:
                    state = "find verb"
                elif word.startswith("/") and state == "find verb":
                    state = "find other resource"
                elif (
                    word.startswith("/")
                    and state == "find other resource"
                    and count_other_resources > 0
                ):
                    state = "find start"
                    count_other_resources = 0
                elif (
                    state == "find other resource"
                    and term
                    and term == other_resource.term
                ):
                    return True
                elif term and state == "find other resource":
                    count_other_resources += 1

        return False

    def drop_from_block(self):
        self.block.drop_resource(self)


def get_type_id(x):
    return (
        x
        if isinstance(x, str)
        else x.type_id
        if isinstance(x, Resource)
        else resource_id_from_class(x)
    )
