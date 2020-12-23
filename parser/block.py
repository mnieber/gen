import typing as T
from parser.line import Line


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
            raise Exception("Expected a {term} resource in block {self.name}")
        return result

    def describe(self):
        result = f"Block: name={self.name}\n"
        for resource in self.resource_by_term.values():
            result += resource.describe(indent=0) + "\n"
        return result
