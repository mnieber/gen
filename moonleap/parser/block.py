import typing as T

from moonleap.parser.line import Line
from ramda import merge
from yaml import Dumper, dump


class Block:
    def __init__(self, name, level, parent_block):
        self.name = name
        self.level = level
        self.parent_block = parent_block
        self._resource_by_term = []
        self.lines: T.List[Line] = []

    def get_resource_by_term(self, include_parents):
        parent_result = (
            self.parent_block.get_resource_by_term(include_parents=True)
            if include_parents and self.parent_block
            else []
        )
        return parent_result + self._resource_by_term

    def get_terms(self, include_parents):
        result = (
            self.parent_block.get_terms(include_parents=True)
            if include_parents and self.parent_block
            else []
        )
        for line in self.lines:
            for term in line.terms:
                if term not in result:
                    result.append(term)
        return result

    def add_resource(self, resource, term):
        resource.block = self
        resource.term = term
        self._resource_by_term.append((term, resource))
        return resource

    def drop_resource(self, resource):
        self._resource_by_term = [
            x for x in self._resource_by_term if x[1] is not resource
        ]

    def find_lines_with_term(self, term):
        return [x for x in self.lines if term in x.terms]

    def describe(self):
        sep = "----------------------------------------------\n"
        result = f"{sep}Block: name={self.name}\n{sep}"
        for term, resource in self._resource_by_term:
            result += dump({str(resource): resource.describe()}) + "\n"
        return result

    def __str__(self):
        return f"Block ({self.name})"
