import os

from titan.react_view_pkg.pkg.builder import Builder

from .helper import Helper
from .tpl import tpls


class FormFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            return {f"Field with FormField": "pass"}

    def build(self):
        __ = self.__ = Helper(
            item_name=self.named_item_term.data,
            mutation_name=self.get_value_by_name("mutation"),
        )
        field_widget_spec = self.widget_spec.find_child_with_place("Field")
        lines = []
        for form_field_name, field_spec in __.fields:
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec
            )
            lines.extend(build_output.lines)
            self.output.graft(build_output)

        context = dict(__=__, form_fields_block=os.linesep.join(lines))
        self.add(
            imports_lines=[tpls.render("form_fields_imports_tpl", context)],
            lines=[tpls.render("form_fields_tpl", context)],
        )

    def _get_field_widget_output(self, form_field_name, field_widget_spec, field_spec):
        from titan.react_view_pkg.pkg.build import build

        with field_widget_spec.memo():
            field_widget_spec.values["form_field_name"] = form_field_name
            field_widget_spec.values["field_spec"] = field_spec
            field_widget_spec.values["helper"] = self.__
            return build(field_widget_spec)


class FormFieldBuilder(Builder):
    def build(self):
        field_spec = self.get_value_by_name("field_spec")
        context = dict(
            field_spec=field_spec,
            name=self.get_value_by_name("form_field_name"),
            __=self.get_value_by_name("helper"),
        )
        self.add(lines=[tpls.render("form_field_tpl", context)])
