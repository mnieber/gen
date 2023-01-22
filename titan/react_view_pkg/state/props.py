from moonleap import create_forward
from moonleap.blocks.verbs import has
from moonleap.utils.case import l0
from titan.react_view_pkg.widgetregistry import get_widget_reg


def state_ts_var(state):
    return l0(state.name)


def create_states_in_modules():
    forwards = []

    for module_name, state_datas in get_widget_reg().states_by_module_name.items():
        for state_term_str, state_data in state_datas.items():
            forwards += [
                create_forward(f"{module_name}:module", has, state_term_str),
            ]

    return forwards
