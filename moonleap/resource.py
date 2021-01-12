import uuid
from importlib import import_module

from moonleap.slctrs import Selector


class Resource:
    def __init__(self):
        self._init()

    def __post_init__(self):
        self._init()

    def _init(self):
        self.id = uuid.uuid4().hex
        self.block = None
        self.term = None
        self._relations = []

    def __repr__(self):
        return self.__class__.__name__

    def get_relations(self):
        return self._relations

    def has_relation(self, rel, resource):
        return resource in Selector([rel]).select_from(self)

    def add_relation(self, relation, resource):
        if not self.has_relation(relation, resource):
            self._relations.append((relation, resource))

        if not resource.has_relation(relation.inv(), self):
            resource._relations.append((relation.inv(), self))


def resolve(resource_type):
    if isinstance(resource_type, str):
        p, type_name = resource_type.rsplit(".", 1)
        return getattr(import_module(p), type_name)
    return resource_type
