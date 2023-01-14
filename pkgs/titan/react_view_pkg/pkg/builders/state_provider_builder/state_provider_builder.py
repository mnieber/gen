from pathlib import Path

from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from moonleap import append_uniq, get_tpl

from .sp_preamble import return_value
from .sp_state_hook import delete_items_data, order_items_data


class StateProviderBuilder(Builder):
    def build(self):
        self.output.has_children_prop = True
        self.output.no_scss = True

        state_provider = self.widget_spec.component
        state = state_provider.state
        containers = state.containers if state else []

        queries = state_provider.queries
        mutations = state_provider.mutations

        functions = dict(
            delete_items_data=delete_items_data,
            order_items_data=order_items_data,
            container_inputs=_container_inputs,
            return_value=lambda data, hint=None: return_value(
                state_provider, containers, data, hint
            ),
            get_data_path=state_provider.get_data_path,
        )

        context = dict(
            containers=containers,
            mutations=mutations,
            queries=queries,
            state=state,
            state_provider=state_provider,
            more_type_specs_to_import=_more_type_specs_to_import(mutations),
            __=functions,
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)


def _container_inputs(containers, named_items=True, named_item_lists=True):
    result = []
    for container in containers:
        if named_items:
            for named_item in container.named_items:
                result.append(named_item)
        if named_item_lists:
            if container.named_item_list:
                result.append(container.named_item_list)
    return result


def _more_type_specs_to_import(mutations):
    types = []
    for mutation in mutations:
        for field in mutation.api_spec.get_inputs(
            ["fk", "relatedSet", "uuid", "uuid[]"]
        ):
            append_uniq(types, field.target_type_spec)
    return types
