from moonleap import Resource, tags


class Service(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["service"])
def create(term, block):
    return [Service(term.data)]


is_ittable = True
