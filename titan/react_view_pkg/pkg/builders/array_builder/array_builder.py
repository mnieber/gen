from pathlib import Path

from moonleap.render.render_template.tpl import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class ArrayBuilder(Builder):
    def build(self):
        item_name = self.ilh.working_item_name
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(
            _get_child_widget_output(self.widget_spec, item_name)
        )
        context = {
            "const_name": const_name,
            "items_expr": self.ilh.item_list_data_path(),
            "item_name": item_name,
            "child_widget_div": child_widget_div,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_const_name(self):
        const_name = self.widget_spec.widget_name
        if not const_name:
            raise Exception("ArrayBuilder requires a widget name")
        return const_name

    def get_spec_extension(self, places):
        self.ilh.get_spec_extension()


def _get_child_widget_output(widget_spec, item_name):
    from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

    child_widget_spec = widget_spec.get_place("Child")
    with child_widget_spec.memo():
        child_widget_spec.div.key = f"{item_name}.id"
        return build_widget_spec(child_widget_spec)
