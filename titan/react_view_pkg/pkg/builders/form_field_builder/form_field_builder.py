from pathlib import Path

from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from moonleap import get_tpl


class FormFieldBuilder(Builder):
    def build(self):
        field_spec = self.widget_spec.values.get("field_spec")
        context = dict(
            field_spec=field_spec,
            name=self.widget_spec.values.get("form_field_name"),
            **self.widget_spec.values.get("parent_context"),
        )
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)
