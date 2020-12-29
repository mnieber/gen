import typing as T

from moonleap.parser.line import Line
from yaml import Dumper, dump


class Block:
    def __init__(self, name):
        self.name = name
        self.resource_by_term = {}
        self.lines: T.List[Line] = []

    def add_resource(self, resource, term):
        if term in self.resource_by_term:
            raise Exception(
                f"Block {self.name} already has a resource with term {term}"
            )
        self.resource_by_term[term] = resource
        return resource

    def get_resource(self, term):
        result = self.resource_by_term.get(term)
        if not result:
            raise Exception(f"Expected a {term} resource in block {self.name}")
        return result

    def drop_resource_by_term(self, term):
        del self.resource_by_term[term]

    def get_resource_by_tag(self, tag):
        for term, res in self.resource_by_term.items():
            if term.tag == tag:
                return res
        return None

    def find_lines_with_term(self, term):
        return [x for x in self.lines if term in x.terms]

    def describe(self):
        sep = "----------------------------------------------\n"
        result = f"{sep}Block: name={self.name}\n{sep}"
        for resource in self.resource_by_term.values():
            result += dump(resource.describe()) + "\n"
        return result


def has_terms_in_same_line(block, term1, term2, is_ordered=True):
    for line in block.lines:
        if term1 in line.terms and term2 in line.terms:
            return (
                line.terms.index(term1) < line.terms.index(term2)
                if is_ordered
                else True
            )

    return False
