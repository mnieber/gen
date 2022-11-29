from moonleap import create_forward
from moonleap.verbs import has, provides
from titan.react_pkg.component.props import get_pipelines


def state_provider_load(state_provider):
    forwards = []
    for component_term, component_data in get_pipelines().get("components", {}).items():
        _check_name(component_term)
        if component_term == state_provider.meta.term.as_normalized_str():
            _get_state_provider(component_term, component_data, forwards)
    return forwards


def _get_state_provider(component_term, component_data, forwards):
    state_datas = component_data.get("states", {})
    for state_term, state_data in state_datas.items():
        _check_name(state_term)
        forwards.append(create_forward(component_term, provides, state_term))
        _get_state(state_term, state_data, forwards)

    items = component_data.get("items_and_lists", [])
    for item_term in items:
        _check_name(item_term)
        forwards.append(create_forward(component_term, provides, item_term))


def _get_state(state_term, state_data, forwards):
    container_datas = state_data.get("containers", {})
    for container_term, container_data in container_datas.items():
        _check_name(container_term)
        forwards.append(create_forward(state_term, has, container_term))
        _get_container(container_term, container_data, forwards)


def _get_container(container_term, container_data, forwards):
    for data_term in container_data.get("data", []):
        forwards.append(create_forward(container_term, has, data_term))
    for bvr_term in container_data.get("bvrs", []):
        forwards.append(create_forward(container_term, has, bvr_term))


def _check_name(name):
    if "_" in name or name != name.lower():
        raise Exception(f"Name should be in kebab-case: {name}")
