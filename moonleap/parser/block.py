import typing as T

from moonleap.parser.line import Line
from moonleap.utils import dict2yaml
from ramda import merge


class Block:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.parent_block = None
        self.child_blocks = []
        self._resources = []
        self.lines: T.List[Line] = []

    def link(self, parent_block):
        self.parent_block = parent_block
        if parent_block:
            parent_block.child_blocks.append(self)

    def get_resources(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []

        if include_children:
            for child_block in self.child_blocks:
                result += child_block.get_resources(include_children=True)

        if include_self:
            result += self._resources

        if include_parents and self.parent_block:
            result += self.parent_block.get_resources(include_parents=True)

        return result

    def get_terms(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []

        if include_children:
            for child_block in self.child_blocks:
                result += child_block.get_terms(include_children=True)

        if include_self:
            for line in self.lines:
                for term in line.terms:
                    if term not in result:
                        result.append(term)

        if include_parents and self.parent_block:
            result += self.parent_block.get_terms(include_parents=True)

        return result

    def add_resource(self, resource, term):
        resource.block = self
        resource.term = term
        self._resources.append(resource)
        return resource

    def drop_resource(self, resource):
        self._resources = [x for x in self._resources if x is not resource]

    def describe(self):
        sep = "----------------------------------------------\n"
        result = f"{sep}Block: name={self.name}\n{sep}"
        for resource in self._resources:
            result += dict2yaml({str(resource): resource.describe()}) + "\n"
        return result

    def __str__(self):
        return f"Block ({self.name})"
