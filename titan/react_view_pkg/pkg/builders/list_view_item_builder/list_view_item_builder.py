from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.bvrs_helper import BvrsHelper


class ListViewItemBuilder(Builder):
    def build(self):
        self.bvrs_helper = BvrsHelper(self.widget_spec, self.ih.working_item_name)
        context = self._get_context()
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def update_widget_spec(self):
        self.bvrs_helper = BvrsHelper(self.widget_spec, self.ih.working_item_name)
        context = self._get_context()
        tpl = get_tpl(Path(__file__).parent / "tpl_div.tsx.j2", context)
        self.widget_spec.div.append_attrs([tpl.get_section("attrs")])
        self.widget_spec.div.append_styles([tpl.get_section("styles")])

    def _get_context(self):
        return {
            **self.bvrs_helper.bvrs_context(),
            "item_name": self.ih.working_item_name,
            "component_name": self.widget_spec.widget_class_name,
        }
