from resources.resource import Resource


class SrcDir(Resource):
    def __init__(self, location):
        self.location = location

    def describe(self, indent=0):
        return " " * indent + f"SrcDir: location={self.location}"


class Builder:
    @staticmethod
    def create(term, line, block):
        return SrcDir(term.data)
