import uuid
from dataclasses import dataclass, field
from importlib import import_module

from moonleap.parser.block import Block
from moonleap.parser.term import Term
from moonleap.rel import Rel
from moonleap.slctrs import Selector


@dataclass
class Resource:
    id: str = field(default_factory=lambda: uuid.uuid4().hex, init=False)
    block: Block = field(default=None, init=False)
    term: Term = field(default=None, init=False)
    _relations: [(Rel, "Resource")] = field(
        default_factory=list, init=False, repr=False
    )

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
