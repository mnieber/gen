from moonleap.utils.queue import Queue


class Tree:
    def __init__(self, name):
        self.elements = []
        self.sources = []
        self.name = name

    @property
    def merged(self):
        result = []
        queue = Queue(lambda x: x, [self])
        for source in queue:
            source_tree = source if source is self else getattr(source, self.name)
            result.extend(source_tree.elements)
            queue.extend(source_tree.sources)
        return result

    def add(self, child):
        if child not in self.elements:
            self.elements.append(child)

    def add_source(self, source):
        if source not in self.sources:
            self.sources.append(source)
