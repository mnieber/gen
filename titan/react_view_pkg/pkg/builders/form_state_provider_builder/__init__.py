from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.get_named_data_term import get_named_item_term

from .helper import Helper
from .tpl import tpls


class FormStateProviderBuilder(Builder):
    def get_spec_extension(self, places):
        if "Children" not in places:
            return {f"Children with FormFields": "pass"}

    def build(self):
        from titan.react_view_pkg.pkg.build import build

        __ = self.__ = Helper(
            item_name=get_named_item_term(self.widget_spec).data,
            mutation_name=self.widget_spec.get_value_by_name("mutation"),
        )

        children_ws = self.widget_spec.find_child_with_place("Children")
        children_build_output = build(children_ws)

        context = dict(__=__)

        self.add(
            imports_lines=[tpls.render("form_sp_imports_tpl", context)],
            preamble_lines=[tpls.render("form_sp_preamble_tpl", context)],
            preamble_hooks_lines=[tpls.render("form_sp_hooks_tpl", context)],
            lines=[
                tpls.render("form_sp_div_open_tpl", context),
                *children_build_output.lines,
                tpls.render("form_sp_div_close_tpl", context),
            ],
        )

        self.output.graft(children_build_output)
