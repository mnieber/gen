from pathlib import Path

import ramda as R
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

from moonleap import get_tpl, u0

from .get_fields import get_fields


class FormStateProviderBuilder(Builder):
    def get_spec_extension(self, places):
        if "Children" not in places:
            return {f"Children with FormFields": "pass"}

    def build(self):
        from titan.react_view_pkg.pkg.build import build

        context = self.get_context()
        children_ws = self.widget_spec.get_place("Children")
        children_build_output = build(children_ws)

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

        self.add(
            lines=[
                tpl.get_section("div_open"),
                *children_build_output.lines,
                tpl.get_section("div_close"),
            ],
        )

        self.output.graft(children_build_output)

    def get_context(self):
        component = self.widget_spec.root.component
        mutation = R.head(component.mutations).api_spec

        item_name = self.ih.array_item_name
        assert item_name

        fields = (
            get_fields(mutation, component.widget_spec.values.get("fields"))
            if mutation
            else []
        )

        return dict(
            item_name=item_name,
            type_spec=get_type_reg().get(u0(item_name) + "Form"),
            mutation=mutation,
            fields=fields,
            uuid_fields=[
                x for x in fields if x[1].field_type == "uuid" and x[1].target
            ],
            validated_fields=_get_validated_fields(fields),
            get_initial_value=_get_initial_value,
        )


def _get_initial_value(field_spec):
    if field_spec.field_type == "boolean":
        return "false"
    return "null"


def _get_validated_fields(fields):
    result = []
    for name, field_spec in fields:
        if (
            not field_spec.is_optional("client")
            and not field_spec.field_type == "boolean"
        ):
            result.append((name, field_spec))
    return result
