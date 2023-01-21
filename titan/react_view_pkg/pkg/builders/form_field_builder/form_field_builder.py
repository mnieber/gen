from pathlib import Path

from moonleap import get_tpl
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class FormFieldBuilder(Builder):
    type = "FormField"

    def build(self):
        field_spec = self.get_value("field_spec")
        context = dict(
            field_spec=field_spec,
            name=self.get_value("form_field_name"),
            **self.get_value("parent_context"),
        )
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)
