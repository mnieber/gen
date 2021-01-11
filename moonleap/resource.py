import uuid

import yaml

from moonleap.parser.term import Term
from moonleap.utils import resource_id_from_class


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.block = None
        self.term = None
        self._children_by_type = {}
        self._parents_by_type = {}

    def __str__(self):
        return self.__class__.__name__

    def children_of_type(self, child_resource_type):
        return self._children_by_type.setdefault(child_resource_type, [])

    def parents_of_type(self, parent_resource_type):
        return self._parents_by_type.setdefault(parent_resource_type, [])

    def add_child(self, child_resource):
        children = self.children_of_type(child_resource.__class__)
        if child_resource not in children:
            children.append(child_resource)
            return True
        return False

    def add_parent(self, parent_resource):
        parents = self.parents_of_type(parent_resource.__class__)
        if parent_resource not in parents:
            parents.append(parent_resource)
            return True
        return False

    def parent_of_type(self, resource_type):
        parents = self.parents_of_type(resource_type)
        if not parents:
            return None

        if len(parents) > 1:
            raise Exception(
                f"Expected a single parent of type {resource_type} in {self}"
            )

        return parents[0]

    def child_of_type(self, resource_type):
        children = self.children_of_type(resource_type)
        if not children:
            return None

        if len(children) > 1:
            raise Exception(
                f"Expected a single child of type {resource_type} in {self}"
            )

        return children[0]

    @property
    def type_id(self):
        return resource_id_from_class(self.__class__)

    @property
    def vendor(self):
        return self.type_id.split(".")[0]

    @property
    def module(self):
        return self.type_id.split(".")[1]

    def drop_from_block(self):
        self.block.drop_resource(self)
