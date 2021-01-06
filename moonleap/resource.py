import uuid

import yaml

from moonleap.parser.term import Term
from moonleap.utils import resource_id_from_class


class Resource:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.block = None
        self.line = None
        self.term = None
        self._children_by_type = {}
        self._parents_by_type = {}

    def __str__(self):
        return self.__class__.__name__

    def get_children_by_type(self, child_resource_type):
        return self._children_by_type.setdefault(child_resource_type, [])

    def get_parents_by_type(self, parent_resource_type):
        return self._parents_by_type.setdefault(parent_resource_type, [])

    def add_child(self, child_resource):
        children = self.get_children_by_type(child_resource.__class__)
        if child_resource not in children:
            children.append(child_resource)
            return True
        return False

    def add_parent(self, parent_resource):
        parents = self.get_parents_by_type(parent_resource.__class__)
        if parent_resource not in parents:
            parents.append(parent_resource)
            return True
        return False

    def parent_of_type(self, resource_type):
        parents = self.get_parents_by_type(resource_type)
        if not parents:
            return None

        if len(parents) > 1:
            raise Exception(
                f"Expected a single parent of type {resource_type} in {self}"
            )

        return parents[0]

    def parents_of_type(self, resource_type):
        parents = self.get_parents_by_type(resource_type)
        if not parents:
            return []

        if not isinstance(parents, list):
            raise Exception(
                f"Expected a list of parents for type {resource_type} in {self}"
            )

        return parents

    def child_of_type(self, resource_type):
        children = self.get_children_by_type(resource_type)
        if not children:
            return None

        if len(children) > 1:
            raise Exception(
                f"Expected a single child of type {resource_type} in {self}"
            )

        return children[0]

    def children_of_type(self, resource_type):
        children = self.get_children_by_type(resource_type)
        if not children:
            return []

        if not isinstance(children, list):
            raise Exception(
                f"Expected a list of children for type {resource_type} in {self}"
            )

        return children

    def describe(self):
        result = {}
        for child_type, children in self._children_by_type.items():
            result[str(child_type)] = [child.describe() for child in children]
        return result

    def dump(self):
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

    def drop_from_block(self):
        self.block.drop_resource(self)


# Don't inline, it will create problems with the closure around parent_type
def create_prop_for_parents(parent_type, is_list):
    return (
        property(lambda self: self.parents_of_type(parent_type))
        if is_list
        else property(lambda self: self.parent_of_type(parent_type))
    )


# Don't inline, it will create problems with the closure around parent_type
def create_prop_for_children(child_type, is_list):
    return (
        property(lambda self: self.children_of_type(child_type))
        if is_list
        else property(lambda self: self.child_of_type(child_type))
    )
