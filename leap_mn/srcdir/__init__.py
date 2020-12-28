from leap_mn.resource import Resource


class SrcDir(Resource):
    def __init__(self, location):
        self.location = location

    def describe(self, indent=0):
        return " " * indent + f"SrcDir: location={self.location}"


def create(term, line, block):
    return SrcDir(term.data)


create_rule_by_tag = {
    "src-dir": create,
}
