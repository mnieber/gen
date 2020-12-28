from leap_mn.resource import Resource


class Pytest(Resource):
    def __init__(self):
        pass

    def describe(self, indent=0):
        return " " * indent + f"Pytest"


def create(term, line, block):
    return Pytest()


create_rule_by_tag = {
    "pytest": create,
}
