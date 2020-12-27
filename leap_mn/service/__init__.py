from leap_mn.resource import Resource


class Service(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self, indent=0):
        return " " * indent + f"Service: name={self.name}"


def create(term, line, block):
    return Service(term.data)
