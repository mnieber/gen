import typing as T
from dataclasses import dataclass, field

from moonleap.resource.rel import Rel


@dataclass
class DocMeta:
    props: [T.Union[str, T.Callable]] = field(default_factory=lambda: [])
    private_rels: [Rel] = field(default_factory=lambda: [])

    def doc_prop(self, x):
        self.props.append(x)
        return self

    def private_rel(self, x):
        self.private_rels.append(x)
        return self

    def add(self, rhs):
        self.props.extend(rhs.props)
        self.private_rels.extend(rhs.private_rels)


@dataclass(frozen=True)
class Prop:
    get_value: T.Callable = None
    set_value: T.Callable = None
    add_value: T.Callable = None
    update_doc_meta: T.Callable = None
