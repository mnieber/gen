from leap_mn.resource import Resource


class Makefile(Resource):
    def __init__(self):
        self.rules = []


def create(term, line, block):
    return Makefile()


def add_to_makefile(rule):
    def action(tool_term, makefile_term, line, block):
        block.get_resource("makefile").rules.append(rule)

    return action
