from moonleap import Resource, tags


class Project(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["project"])
def create(term, block):
    return [Project(term.data)]


is_ittable = True
