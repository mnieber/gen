from pathlib import Path

from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from moonleap import append_uniq, get_tpl

from .get_container_data import (
    delete_items_data,
    get_container_inputs,
    order_items_data,
)
from .get_return_value import get_return_value


class StateProviderBuilder(Builder):
    def build(self):
        self.output.has_children_prop = True
        self.output.no_scss = True

        state_provider = self.widget_spec.component
        state = state_provider.state
        containers = state.containers if state else []

        queries = state_provider.queries
        mutations = state_provider.mutations

        context = dict(
            containers=containers,
            mutations=mutations,
            queries=queries,
            state=state,
            state_provider=state_provider,
            more_type_specs_to_import=_more_type_specs_to_import(mutations),
            delete_items_data=delete_items_data,
            order_items_data=order_items_data,
            get_container_inputs=get_container_inputs,
            get_return_value=lambda data, hint=None: get_return_value(
                state_provider, containers, data, hint
            ),
            get_data_path=state_provider.get_data_path,
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)


def _more_type_specs_to_import(mutations):
    types = []
    for mutation in mutations:
        for field in mutation.api_spec.get_inputs(
            ["fk", "relatedSet", "uuid", "uuid[]"]
        ):
            append_uniq(types, field.target_type_spec)
    return types
