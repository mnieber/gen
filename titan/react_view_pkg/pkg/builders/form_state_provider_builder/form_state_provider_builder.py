from pathlib import Path

import ramda as R

from moonleap import get_tpl, u0
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

from .get_fields import get_fields


class FormStateProviderBuilder(Builder):
    def get_spec_extension(self, places):
        if "Children" not in places:
            return {f"Children with FormFields": "pass"}

    def build(self):
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        context = self.get_context()
        children_ws = self.widget_spec.get_place("Children")
        children_build_output = build_widget_spec(children_ws)

        tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        add_tpl_to_builder(tpl, self)

        self.output.add(
            lines=[
                tpl.get_section("div_open"),
                *children_build_output.lines,
                tpl.get_section("div_close"),
            ],
        )

        self.output.graft(children_build_output)

    def get_context(self):
        widget_spec = self.widget_spec.root

        # We expect the component to have a pipeline that returns
        # a mutation or an edit:behavior.
        mutation, editing_bvr = get_form_mutation_or_bvr(widget_spec)
        fields = (
            get_fields(mutation.api_spec, widget_spec.field_names) if mutation else []
        )

        item_name = self.ih.working_item_name
        assert item_name

        return dict(
            item_name=item_name,
            type_spec=get_type_reg().get(u0(item_name) + "Form"),
            mutation=mutation,
            editing_bvr=editing_bvr,
            fields=fields,
            uuid_fields=[
                x for x in fields if x[1].field_type == "uuid" and x[1].target
            ],
            validated_fields=_get_validated_fields(fields),
            get_initial_value=_get_initial_value,
        )


def get_form_mutation_or_bvr(widget_spec):
    mutation = None
    editing_bvr = None
    for pipeline in widget_spec.pipelines:
        pipeline_source = pipeline.source
        if pipeline_source.meta.term.tag == "mutation":
            mutation = pipeline_source
        if pipeline_source.meta.term.tag == "props":
            prop = pipeline.resources[1]
            if prop.typ.meta.term.tag == "editing":
                editing_bvr = prop.typ
                mutation = editing_bvr.mutation
    return mutation, editing_bvr


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
