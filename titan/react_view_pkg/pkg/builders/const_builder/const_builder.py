import os
from pathlib import Path

from moonleap.render.tpls import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class ConstBuilder(Builder):
    def build(self):
        const_name = self._get_const_name()
        child_widget_output = _get_child_widget_output(self.widget_spec)
        child_widget_div = os.linesep.join(child_widget_output.lines)
        self.output.graft(child_widget_output)
        context = {
            "const_name": const_name,
            "child_widget_div": child_widget_div,
        }

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_const_name(self):
        const_name = self.widget_spec.widget_name
        if not const_name:
            raise Exception("ArrayBuilder requires a widget name")
        return const_name


def _get_child_widget_output(widget_spec):
    from titan.react_view_pkg.pkg.build import build

    child_widget_spec = widget_spec.find_child_with_place("Child")
    with child_widget_spec.memo():
        return build(child_widget_spec)
