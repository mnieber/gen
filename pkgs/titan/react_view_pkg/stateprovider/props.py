from moonleap import append_uniq, create_forward
from moonleap.blocks.verbs import provides
from pkgs.titan.react_pkg.component.props import component_mutations


def state_provider_load(state_provider):
    forwards = []
    widget_spec = state_provider.widget_spec

    for state_term_str in widget_spec.src_dict.get("__states__", []):
        forwards.append(create_forward(state_provider, provides, state_term_str))

    for pipeline in state_provider.pipelines:
        for res in pipeline.resources:
            if res.meta.term.tag in ("item", "item~list"):
                if res.meta.term.is_title:
                    forwards.append(create_forward(state_provider, provides, res))

    return forwards


def state_provider_mutations(state_provider):
    mutations = component_mutations(state_provider)
    state = state_provider.state
    containers = state.containers if state else []
    for container in containers:
        if delete_items_mutation := container.delete_items_mutation:
            append_uniq(mutations, delete_items_mutation)
        if delete_item_mutation := container.delete_item_mutation:
            append_uniq(mutations, delete_item_mutation)
        if order_items_mutation := container.order_items_mutation:
            append_uniq(mutations, order_items_mutation)
    return mutations
