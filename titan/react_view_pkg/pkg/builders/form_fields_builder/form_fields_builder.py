import os
from pathlib import Path

import ramda as R

from moonleap import get_tpl, u0
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder


class FormFieldsBuilder(Builder):
    type = "FormFields"

    def get_spec_extension(self, places):
        if "Field" not in places:
            return {f"Field with FormField": "pass"}

    def build(self):
        context = self.get_context()

        field_widget_spec = self.widget_spec.get_place("Field")
        lines = []
        for form_field_name, field_spec in context["fields"]:
            if field_spec.field_type in ("uuid",):
                continue
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec, context
            )
            lines.extend(build_output.lines)
            self.output.graft(build_output)
        context["form_fields_block"] = os.linesep.join(lines)

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def get_context(self):
        return dict(
            item_name=self.ih.working_item_name,
            fields=self.widget_spec.get_form_data(recurse=True).fields,
            get_slug_src=_get_slug_src,
            get_label=_get_label,
            get_display_field_name=_get_display_field_name,
        )

    def _get_field_widget_output(
        self, form_field_name, field_widget_spec, field_spec, context
    ):
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        with field_widget_spec.memo(["values"]):
            field_widget_spec.values["form_field_name"] = form_field_name
            field_widget_spec.values["field_spec"] = field_spec
            field_widget_spec.values["parent_context"] = context
            return build_widget_spec(field_widget_spec)


def _get_slug_src(fields, field_spec):
    slug_sources = [name for name, field_spec in fields if field_spec.is_slug_src]
    return R.head(slug_sources) or "Moonleap Todo: slug_src"


def _get_label(name):
    return " ".join([u0(x) for x in name.split(".")])


def _get_display_field_name(type_spec):
    return type_spec.display_field.name if type_spec.display_field else "id"
