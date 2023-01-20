from pathlib import Path

from moonleap import append_uniq, get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from .get_container_data import (
    delete_items_data,
    get_container_inputs,
    order_items_data,
    save_item_data,
)
from .get_return_value import get_return_value


class StateProviderBuilder(Builder):
    def build(self):
        self.widget_spec.root.add_tag("has_children_prop")
        self.widget_spec.root.add_tag("no_scss")

        state_provider = self.widget_spec.component
        state = state_provider.state
        containers = state.containers if state else []

        queries = self.widget_spec.queries
        mutations = _get_mutations(self.widget_spec, state)

        context = dict(
            state_provider=state_provider,
            containers=containers,
            mutations=mutations,
            queries=queries,
            state=state,
            widget_spec=self.widget_spec,
            more_type_specs_to_import=_more_type_specs_to_import(mutations),
            delete_items_data=delete_items_data,
            order_items_data=order_items_data,
            save_item_data=save_item_data,
            get_container_inputs=get_container_inputs,
            get_return_value=lambda data, hint=None: get_return_value(
                state_provider, containers, data, hint
            ),
            get_data_path=self.widget_spec.get_data_path,
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)


def _get_mutations(widget_spec, state):
    mutations = widget_spec.mutations
    containers = state.containers if state else []
    for container in containers:
        if delete_items_mutation := container.delete_items_mutation:
            append_uniq(mutations, delete_items_mutation)
        if delete_item_mutation := container.delete_item_mutation:
            append_uniq(mutations, delete_item_mutation)
        if save_item_mutation := container.save_item_mutation:
            append_uniq(mutations, save_item_mutation)
        if order_items_mutation := container.order_items_mutation:
            append_uniq(mutations, order_items_mutation)
    return mutations


def _more_type_specs_to_import(mutations):
    types = []
    for mutation in mutations:
        for field in mutation.api_spec.get_inputs(
            ["fk", "relatedSet", "uuid", "uuid[]"]
        ):
            append_uniq(types, field.target_type_spec)
    return types
