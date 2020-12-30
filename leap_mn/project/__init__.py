from moonleap.resource import Resource


class Project(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, line, block):
    return [Project(term.data)]


is_ittable = True
tags = ["project"]
