import typing as T

import ramda as R
from moonleap.parser.line import Line


class Block:
    def __init__(self, name, level):
        self.name = name
        self.level = level
        self.parent_block = None
        self.child_blocks = []
        self._resources = []
        self.lines: T.List[Line] = []

    def describes(self, term):
        return term in self.lines[0].terms

    def mentions(self, term):
        return term in self.get_terms()

    def get_resource(self, term):
        resources = [x for x in self._resources if x.term == term]
        return resources[0] if resources else None

    def link(self, parent_block):
        self.parent_block = parent_block
        if parent_block:
            parent_block.child_blocks.append(self)

    def get_blocks(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []

        if include_parents and self.parent_block:
            result += self.parent_block.get_blocks(include_parents=True)

        if include_self:
            result += [self]

        if include_children:
            for child_block in self.child_blocks:
                result += child_block.get_blocks(include_children=True)

        return result

    def get_resources(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []
        for block in self.get_blocks(include_self, include_children, include_parents):
            result += block._resources

        return R.uniq(result)

    def get_terms(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []
        for block in self.get_blocks(include_self, include_children, include_parents):
            for line in block.lines:
                for term in line.terms:
                    if term not in result:
                        result.append(term)
        return result

    def add_resource(self, resource):
        if self.get_resource(resource.term):
            raise Exception(
                f"Block {self.name} already has an resource for term {resource.term}"
            )

        self._resources.append(resource)

    def drop_resource(self, resource):
        self._resources = [x for x in self._resources if x is not resource]

    def __repr__(self):
        return f"Block ({self.name})"
