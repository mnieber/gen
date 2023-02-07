from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from .get_return_value import get_return_value


class StateProviderBuilder(Builder):
    type = "StateProvider"

    def build(self):
        self.widget_spec.root.add_tag("has_children_prop")
        self.widget_spec.root.add_tag("no_scss")

        state_provider = self.widget_spec.component
        states = state_provider.states

        context = dict(
            state_provider=state_provider,
            states=states,
            widget_spec=self.widget_spec,
            get_container_inputs=get_container_inputs,
            get_return_value=lambda state, data, hint=None: get_return_value(
                state_provider, state, data, hint
            ),
            get_data_path=self.widget_spec.get_data_path,
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)


def get_container_inputs(containers, named_items=True, named_item_lists=True):
    result = []
    for container in containers:
        if named_items:
            for named_item in container.named_items:
                result.append(named_item)
        if named_item_lists:
            if container.named_item_list:
                result.append(container.named_item_list)
    return result
