from moonleap.resource import Resource


class Pytest(Resource):
    def __init__(self):
        pass


def create(term, line, block):
    return [Pytest()]


tags = ["pytest"]
