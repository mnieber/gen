import os

from moonleap import create_forward, get_session, load_yaml
from moonleap.verbs import connects, has, provides


def state_provider_load(state_provider):
    spec_dir = get_session().spec_dir
    fn = os.path.join(spec_dir, "pipelines.yaml")
    if os.path.exists(fn):
        component_datas = load_yaml(fn).get("components", {})
        return _get_forwards(state_provider, component_datas)


def _get_forwards(state_provider, component_datas):
    forwards = []
    for component_term, component_data in component_datas.items():
        _check_name(component_term)
        if component_term == state_provider.meta.term.as_normalized_str():
            _get_state_provider(component_term, component_data, forwards)
    return forwards


def _get_state_provider(component_term, component_data, forwards):
    pipeline_datas = component_data.get("pipelines", {})
    for pipeline_term, pipeline_data in pipeline_datas.items():
        _check_name(pipeline_term)
        forwards.append(create_forward(component_term, has, pipeline_term))
        _get_pipeline(pipeline_term, pipeline_data, forwards)

    state_datas = component_data.get("states", {})
    for state_term, state_data in state_datas.items():
        _check_name(state_term)
        forwards.append(create_forward(component_term, provides, state_term))
        _get_state(state_term, state_data, forwards)

    items = component_data.get("items_and_lists", [])
    for item_term in items:
        _check_name(item_term)
        forwards.append(create_forward(component_term, provides, item_term))


def _get_pipeline(pipeline_term, pipeline_data, forwards):
    for term in pipeline_data:
        forwards.append(create_forward(pipeline_term, connects, term))


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
