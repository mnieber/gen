import typing as T

from moonleap.parser.line import Line
from moonleap.parser.term import create_generic_terms


class Block:
    def __init__(self, name, level, context_names):
        self.name = name
        self.context_names = context_names
        self.level = level
        self.parent_block = None
        self.child_blocks = []
        self._resource_by_term = []
        self.lines: T.List[Line] = []

    def describes(self, term):
        generic_terms = create_generic_terms(term)
        return term in self.lines[0].terms or (
            [x for x in generic_terms if x in self.lines[0].terms]
            and [line for line in self.lines if term in line.terms]
        )

    def get_resource(self, term):
        resources = [x[1] for x in self._resource_by_term if x[0] == term]
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

    def get_resource_by_term(self):
        return [x for x in self._resource_by_term]

    def get_terms(self):
        result = []
        for line in self.lines:
            for term in line.terms:
                if term not in result:
                    result.append(term)
        return result

    def add_resource_for_term(self, resource, term, is_owner):
        if self.get_resource(term):
            raise Exception(
                f"Block {self.name} already has an resource for term {term}"
            )

        self._resource_by_term.append((term, resource, is_owner))

    def drop_resource(self, resource):
        self._resource_by_term = [
            x for x in self._resource_by_term if x[1] is not resource
        ]

    def __repr__(self):
        return f"Block ({self.name})"


def get_extended_context_names(root_block):
    context_names = []
    for block in root_block.get_blocks(include_children=True):
        for context_name in block.context_names:
            if context_name not in context_names:
                context_names.append(context_name)
    return context_names
