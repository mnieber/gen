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
        for term, resource in self._resource_by_term:
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
            result += dump(resource.describe()) + "\n"
        return result

    def __str__(self):
        return f"Block ({self.name})"


def get_resource_by_tag(resource_by_term, tag):
    for term, res in resource_by_term.items():
        if term.tag == tag:
            return res
    return None

    # def get_resource(self, term, raise_if_not_found=True):
    #     result = self.resource_by_term.get(term)
    #     if not result and self.parent_block:
    #         result = self.parent_block.get_resource(term, raise_if_not_found=False)

    #     if raise_if_not_found and not result:
    #         raise Exception(f"Expected a {term} resource in block {self.name}")

    #     return result
