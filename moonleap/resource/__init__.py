import random
import typing as T
import uuid
from dataclasses import dataclass, field
from importlib import import_module

from moonleap.resource.memfield import MemField
from moonleap.resource.memfun import MemFun
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel
from moonleap.resource.slctrs import Selector

# Use a fixed seed for the id generator
rd = random.Random()
rd.seed(0)
uuid.uuid4 = lambda: uuid.UUID(int=rd.getrandbits(128))


def find_extension(resource, item):
    extensions = resource.__dict__.get("_extensions", {})
    for extension in extensions:
        for base_type in extension.__mro__:
            for prop_name, p in base_type.__dict__.items():
                if prop_name == item:
                    return p
    return None


@dataclass
class Resource:
    id: str = field(default_factory=lambda: uuid.uuid4().hex, init=False)

    _relations: T.List[T.Tuple[Rel, "Resource"]] = field(
        default_factory=list, init=False, repr=False
    )

    _extensions: T.List[T.Any] = field(default_factory=list, init=False, repr=False)

    def extend(self, extension):
        self._extensions.append(extension)

    def __getattr__(self, item):
        p = find_extension(self, item)
        if p is None:
            raise AttributeError

        if isinstance(p, Prop):
            return p.get_value(self)
        elif isinstance(p, MemFun):
            return lambda *args, **kwargs: p.f(self, *args, **kwargs)
        elif isinstance(p, MemField):
            private_name = "_" + item
            if not hasattr(self, private_name):
                setattr(self, private_name, p.f())
            return getattr(self, private_name)
        raise Exception(f"Unknown extension {p}")

    def __setattr__(self, item, value):
        p = find_extension(self, item)
        if p is None:
            return super().__setattr__(item, value)

        if isinstance(p, Prop):
            if not p.set_value:
                raise Exception(f"Property '{item}' does not support set_value")
            return p.set_value(self, value)
        elif isinstance(p, MemField):
            private_name = "_" + item
            setattr(self, private_name, value)
        raise Exception(f"Unknown extension {p}")

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
