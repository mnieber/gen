class Resource:
    def describe(self, indent=0):
        return " " * indent + str(type(self).__name__)

    def build(self, resources):
        pass
