import typing as T

from moonleap.parser.line import Line
from moonleap.utils import dict2yaml
from ramda import merge


class Block:
    def __init__(self, name, level, parent_block):
        self.name = name
        self.level = level
        self.parent_block = parent_block
        self._resources = []
        self.lines: T.List[Line] = []

    def get_resources(self, include_parents):
        parent_result = (
            self.parent_block.get_resources(include_parents=True)
            if include_parents and self.parent_block
            else []
        )
        return parent_result + self._resources

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
        self._resources.append(resource)
        return resource

    def drop_resource(self, resource):
        self._resources = [x for x in self._resources if x is not resource]

    def find_lines_with_term(self, term):
        return [x for x in self.lines if term in x.terms]

    def describe(self):
        sep = "----------------------------------------------\n"
        result = f"{sep}Block: name={self.name}\n{sep}"
        for resource in self._resources:
            result += dict2yaml({str(resource): resource.describe()}) + "\n"
        return result

    def __str__(self):
        return f"Block ({self.name})"
