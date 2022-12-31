from pathlib import Path

from moonleap import append_uniq, get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from .sp_preamble import return_value
from .sp_state_hook import delete_items_data, order_items_data


class StateProviderBuilder(Builder):
    def build(self):
        self.output.has_children = True
        self.output.no_scss = True

        state_provider = self.widget_spec.component
        state = state_provider.state
        containers = state.containers if state else []
        pipelines = state_provider.pipelines

        queries, mutations = [], []
        _get_endpoints_from_pipelines(pipelines, queries, mutations)
        _get_mutations_from_containers(containers, mutations)

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


def _get_endpoints_from_pipelines(pipelines, queries, mutations):
    for pipeline in pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "query":
            append_uniq(queries, pipeline_source)
        if pipeline_source.meta.term.tag == "mutation":
            append_uniq(mutations, pipeline_source)


def _get_mutations_from_containers(containers, mutations):
    for container in containers:
        if delete_items_mutation := container.delete_items_mutation:
            append_uniq(mutations, delete_items_mutation)
        if delete_item_mutation := container.delete_item_mutation:
            append_uniq(mutations, delete_item_mutation)
        if order_items_mutation := container.order_items_mutation:
            append_uniq(mutations, order_items_mutation)


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