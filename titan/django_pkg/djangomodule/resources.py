from dataclasses import dataclass
from moonleap import (
    RenderMixin,
    Resource,
    TemplateDirMixin,
)


@dataclass
class DjangoModule(TemplateDirMixin, RenderMixin, Resource):
    name: str
    has_graphql_schema: bool = False
