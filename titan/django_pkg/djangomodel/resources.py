import typing as T
from dataclasses import dataclass

from moonleap import RenderMixin, Resource
from titan.typespec.type_spec import TypeSpec


@dataclass
class DjangoModel(RenderMixin, Resource):
    name: str
    kebab_name: str
    type_spec: T.Optional[TypeSpec] = None
