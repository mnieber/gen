from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from .get_data_path import get_data_path


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
            queries=self.widget_spec.queries,
            widget_spec=self.widget_spec,
            get_data_path=lambda data, state=None, hint=None: get_data_path(
                state_provider, data, state, hint
            ),
        )

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)
