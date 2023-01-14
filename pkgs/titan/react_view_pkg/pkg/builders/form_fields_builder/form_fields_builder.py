import os
from pathlib import Path

import ramda as R
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.react_view_pkg.pkg.builders.form_state_provider_builder.get_fields import (
    get_fields,
)

from moonleap import get_tpl, u0


class FormFieldsBuilder(Builder):
    def get_spec_extension(self, places):
        if "Field" not in places:
            return {f"Field with FormField": "pass"}

    def build(self):
        context = self.get_context()

        field_widget_spec = self.widget_spec.get_place("Field")
        lines = []
        for form_field_name, field_spec in context["fields"]:
            build_output = self._get_field_widget_output(
                form_field_name, field_widget_spec, field_spec, context
            )
            lines.extend(build_output.lines)
            self.output.graft(build_output)
        context["form_fields_block"] = os.linesep.join(lines)

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

    def get_context(self):
        component = self.widget_spec.root.component
        item_name = self.ih.array_item_name
        mutation = R.head(component.mutations).api_spec
        fields = (
            get_fields(mutation, self.widget_spec.values.get("fields"))
            if mutation
            else []
        )

        return dict(
            item_name=item_name,
            fields=fields,
            get_slug_src=_get_slug_src,
            get_label=_get_label,
            get_display_field_name=_get_display_field_name,
        )

    def _get_field_widget_output(
        self, form_field_name, field_widget_spec, field_spec, context
    ):
        from titan.react_view_pkg.pkg.build import build

        with field_widget_spec.memo():
            field_widget_spec.values["form_field_name"] = form_field_name
            field_widget_spec.values["field_spec"] = field_spec
            field_widget_spec.values["parent_context"] = context
            return build(field_widget_spec)


def _get_slug_src(fields, field_spec):
    slug_sources = [name for name, field_spec in fields if field_spec.is_slug_src]
    return R.head(slug_sources) or "Moonleap Todo: slug_src"


def _get_label(name):
    return u0(name.replace(".", " "))


def _get_display_field_name(type_spec):
    return type_spec.display_field.name if type_spec.display_field else "id"
