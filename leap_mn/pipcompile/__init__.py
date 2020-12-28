from leap_mn.resource import Resource


class PipCompile(Resource):
    def __init__(self):
        pass


def create(term, line, block):
    return PipCompile()


create_rule_by_tag = {
    "pip-compile": create,
}

update_rules = [
    (None, "dockerfile"),
    ("leap_mn.makefile", "makefile"),
]
