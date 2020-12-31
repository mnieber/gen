from moonleap.resource import Resource


class MakefileRule(Resource):
    def __init__(self, text):
        self.text = text

    def describe(self):
        return dict(text=self.text)


def create(term, block):
    return [Layer(name=term.data)]


tags = ["layer"]
