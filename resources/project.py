from resources.resource import Resource


class Project(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self, indent=0):
        return " " * indent + f"Project: name={self.name}"


class Builder:
    @staticmethod
    def create(term, line, block):
        return Project(term.data)
