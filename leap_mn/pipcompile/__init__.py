from leap_mn.resource import Resource


class PipCompile(Resource):
    def __init__(self):
        pass


def create(self, term, line, block):
    return PipCompile()
