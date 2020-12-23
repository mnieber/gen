class Term:
    def __init__(self, data, tag):
        self.data = data
        self.tag = tag

    def __str__(self):
        return f"Term tag={self.tag} data={self.data}"

    def __hash__(self):
        return hash((self.tag, self.data))
