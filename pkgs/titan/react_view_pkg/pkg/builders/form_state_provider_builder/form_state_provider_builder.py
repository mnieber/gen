from pathlib import Path

import ramda as R
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from moonleap import get_tpl

from .helper import Helper


class FormStateProviderBuilder(Builder):
    def get_spec_extension(self, places):
        if "Children" not in places:
            return {f"Children with FormFields": "pass"}

    def build(self):
        from titan.react_view_pkg.pkg.build import build

        component = self.widget_spec.root.component
        __ = self.__ = Helper(
            item_name=self.ih.array_item_name,
            mutation=R.head(component.mutations),
            fields=self.widget_spec.values.get("fields"),
        )

        children_ws = self.widget_spec.get_place("Children")
        children_build_output = build(children_ws)

        context = dict(__=__)
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

        self.add(
            lines=[
                tpl.get_section("div_open"),
                *children_build_output.lines,
                tpl.get_section("div_close"),
            ],
        )

        self.output.graft(children_build_output)
