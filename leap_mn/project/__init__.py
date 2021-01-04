from moonleap import Resource


class Project(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def describe(self):
        return dict(name=self.name)


def create(term, block):
    return [Project(term.data)]


is_ittable = True
tags = ["project"]
