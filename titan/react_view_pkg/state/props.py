from moonleap import create_forward
from moonleap.utils.case import l0
from moonleap.verbs import has


def state_ts_var(state):
    return l0(state.name)


def load_states(widget_reg):
    forwards = []
    for module_name, state_datas in widget_reg.states_by_module_name.items():
        module_term_str = f"{module_name}:module"
        forwards += [
            create_forward(":react-app", has, module_term_str),
        ]
        for state_term_str, state_data in state_datas.items():
            forwards += [
                create_forward(module_term_str, has, module_term_str),
            ]
            _get_state(state_term_str, state_data, forwards)
    return forwards


def _get_state(state_term_str, state_data, forwards):
    container_datas = state_data.get("containers", {})
    for container_term, container_data in container_datas.items():
        _check_name(container_term)
        forwards.append(create_forward(state_term_str, has, container_term))
        _get_container(container_term, container_data, forwards)


def _get_container(container_term, container_data, forwards):
    for data_term in container_data.get("data", []):
        forwards.append(create_forward(container_term, has, data_term))
    for bvr_term in container_data.get("bvrs", []):
        forwards.append(create_forward(container_term, has, bvr_term))


def _check_name(name):
    if "_" in name or name != name.lower():
        raise Exception(f"Name should be in kebab-case: {name}")
