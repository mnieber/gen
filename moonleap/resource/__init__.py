import random
import typing as T
import uuid
from dataclasses import dataclass, field
from importlib import import_module

from moonleap.resource.prop import DocMeta
from moonleap.resource.rel import Rel
from moonleap.resource.slctrs import Selector

# Use a fixed seed for the id generator
rd = random.Random()
rd.seed(0)
uuid.uuid4 = lambda: uuid.UUID(int=rd.getrandbits(128))


@dataclass
class Resource:
    id: str = field(default_factory=lambda: uuid.uuid4().hex, init=False)
    _relations: T.List[T.Tuple[Rel, "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    doc_meta: DocMeta = field(default_factory=lambda: DocMeta(), init=False)

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
