from pathlib import Path

from moonleap import append_uniq, get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class StepperBuilder(Builder):
    def build(self):
        use_uniform_height = self.widget_spec.values.get("uniformHeight")
        item_name = self.ilh.array_item_name
        const_name = self._get_const_name()

        child_widget_div = self.output.graft(
            _get_child_widget_output(self.widget_spec, item_name, use_uniform_height)
        )
        context = {
            "__const_name": const_name,
            "__items_expr": self.ilh.item_list_data_path(),
            "__item_name": item_name,
            "__child_widget_div": child_widget_div,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_const_name(self):
        return f"{self.ilh.array_item_name}Divs"

    def update_widget_spec(self):
        self.ilh.update_widget_spec()
        tpl = get_tpl(Path(__file__).parent / "tpl_div.tsx.j2", {})
        append_uniq(self.widget_spec.root.div.attrs, tpl.get_section("attrs"))


def _get_child_widget_output(widget_spec, item_name, use_uniform_height):
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Child")
    with child_widget_spec.memo():
        child_widget_spec.div.key = f"{item_name}.id"
        if use_uniform_height:
            child_widget_spec.div.append_styles(
                [f"idx === {item_name}Idx ? 'visible' : 'invisible'"]
            )
        return build(child_widget_spec)
