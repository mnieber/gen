import os
from pathlib import Path

import ramda as R
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder

from moonleap import get_tpl

from .helper import Helper


class FormFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            return {f"Field with FormField": "pass"}

    def build(self):
        component = self.widget_spec.root.component
        __ = self.__ = Helper(
            item_name=self.ih.array_item_name,
            mutation=R.head(component.mutations),
        )
        field_widget_spec = self.widget_spec.get_place("Field")
        lines = []
        for form_field_name, field_spec in __.fields:
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec
            )
            lines.extend(build_output.lines)
            self.output.graft(build_output)

        context = dict(__=__, __form_fields_block=os.linesep.join(lines))
        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def _get_field_widget_output(self, form_field_name, field_widget_spec, field_spec):
        from titan.react_view_pkg.pkg.build import build

        with field_widget_spec.memo():
            field_widget_spec.values["form_field_name"] = form_field_name
            field_widget_spec.values["field_spec"] = field_spec
            field_widget_spec.values["helper"] = self.__
            return build(field_widget_spec)
