import os

from moonleap.typespec.type_spec_store import type_spec_store
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)
from titan.react_view_pkg.pkg.create_router_configs_from_chain import (
    create_router_configs_from_chain,
)


def create_router_configs(self, named_component):
    result = create_router_configs_from_chain([])
    url = get_component_base_url(self, self.item_name)
    router_config = create_component_router_config(
        self, named_component=named_component, url=url
    )
    result.append(router_config)

    return result


def get_context(item_view):
    _ = lambda: None
    _.type_spec = type_spec_store().get(item_view.item.item_type.name)

    class Sections:
        def fields(self):
            result = []

            for field_spec in _.type_spec.field_specs:
                if (
                    field_spec.private
                    or field_spec.name in ("id",)
                    or field_spec.field_type in ("slug", "fk", "relatedSet")
                ):
                    continue

                if field_spec.field_type in ("boolean"):
                    value = (
                        f"props.{item_view.item_name}.{field_spec.name} ? 'Yes' : 'No'"
                    )
                else:
                    value = f"props.{item_view.item_name}.{field_spec.name}"

                result.append(f"<div>{field_spec.name}: {{{value}}}</div>")
            return os.linesep.join(" " * 6 + line for line in result)

    return dict(sections=Sections(), _=_)
