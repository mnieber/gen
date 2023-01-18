from moonleap import named
from moonleap.blocks.term import word_to_term
from titan.react_view_pkg.state.resources import Container
from titan.react_view_pkg.widgetregistry import get_widget_reg
from titan.types_pkg.itemlist import ItemList

from .create_resource import create_resource


def hydrate_state(state):
    for module_name, state_datas in get_widget_reg().states_by_module_name.items():
        for state_term_str, state_data in state_datas.items():
            if state.meta.term == word_to_term(state_term_str):
                _get_state(state, state_data)


def _get_state(state, state_data):
    container_datas = state_data.get("__containers__", {})
    for container_term_str, container_data in container_datas.items():
        _check_name(container_term_str)
        state.containers.append(
            _create_container(state, container_term_str, container_data)
        )


def _create_container(state, container_term_str, container_data):
    container = Container(name=word_to_term(container_term_str).data)
    for data_term_str in container_data.get("__data__", []):
        data_term = word_to_term(data_term_str)
        data_res = create_resource(state.meta.block, data_term)
        if isinstance(data_res, named(ItemList)):
            container.named_item_list = data_res

    if not container.named_item_list:
        raise Exception(f"Container should have an item list: {container_data}")

    for bvr_name in _get_state_bvr_names(container_data):
        bvr_term_str = f"{container.item.item_name}:{bvr_name}"
        bvr_term = word_to_term(bvr_term_str)
        bvr = create_resource(state.meta.block, bvr_term)
        container.bvrs.append(bvr)

    return container


def _get_state_bvr_names(container_data):
    bvr_names = container_data.get("__bvrs__", [])
    if "selection" in bvr_names and "highlight" not in bvr_names:
        bvr_names.append("highlight")
    if "drag-and-drop" in bvr_names and "insertion" not in bvr_names:
        bvr_names.append("insertion")
    return bvr_names


def _check_name(name):
    if "_" in name or name != name.lower():
        raise Exception(f"Name should be in kebab-case: {name}")
