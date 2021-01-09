import uuid


class Entity:
    def __init__(self, block, term, resources):
        self.id = uuid.uuid4().hex
        self.block = block
        self.term = term
        self.resources = resources

    def __str__(self):
        return f"Entity({self.term})"
