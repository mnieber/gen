import uuid

import yaml

from moonleap.parser.term import Term, word_to_term
from moonleap.utils import resource_id_from_class


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
        if config.has_children_of_type(self.__class__, child_resource.__class__):
            children = self.children.setdefault(child_resource.key, [])
            if child_resource not in children:
                children.append(child_resource)

        if config.has_parents_of_type(child_resource.__class__, self.__class__):
            parents = child_resource.parents.setdefault(self.key, [])
            if self not in parents:
                parents.append(self)

    def parent(self, resource_type):
        parents = self.parents.get(resource_type)
        if not parents:
            return None

        if len(parents) > 1:
            raise Exception(
                f"Expected a single parent of type {resource_type} in {self}"
            )

        return parents[0]

    def describe(self):
        result = {}
        for child_type, children in self.children.items():
            result[str(child_type)] = [child.describe() for child in children]
        return result

    def dump(self):
        __import__("pudb").set_trace()
        print(yaml.dump(self.describe()))

    @property
    def type_id(self):
        return resource_id_from_class(self.__class__)

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
