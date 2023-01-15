import typing as T
from dataclasses import dataclass, field

from jdoc.moonleap.block import Block
from moonleap.blocks.term import Term
from moonleap.resources.relations.slctrs import RelSelector
from moonleap.utils.get_id import get_id


@dataclass
class ResourceMetaData:
    term: Term
    block: Block
    base_tags: T.List[str]


@dataclass
class Resource:
    id: str = field(default_factory=get_id, init=False, repr=False)
    _relations: T.List[T.Tuple["Rel", "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    _inv_relations: T.List[T.Tuple["Rel", "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )
    meta: T.Optional[ResourceMetaData] = field(
        default_factory=lambda: None, init=False, repr=False
    )

    def __repr__(self):
        return self.__class__.__name__

    def get_relations(self):
        return self._relations

    def get_inv_relations(self):
        return self._inv_relations

    def has_relation(self, rel, resource):
        return resource in RelSelector(rel).select_from(self)

    def add_relation(self, relation, obj_res):
        if not self.has_relation(relation, obj_res):
            self._relations.append((relation, obj_res))
            obj_res._inv_relations.append((relation, self))
