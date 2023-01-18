from pathlib import Path

from moonleap import get_tpl, u0
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg

from .get_fields import get_fields


class FormStateProviderBuilder(Builder):
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
        # We expect the widget_spec to have a "save" pipeline
        mutation, editing_bvr = get_form_mutation_or_bvr(self.widget_spec)

        fields = (
            get_fields(
                mutation.api_spec, self.widget_spec.get_field_names(recurse=True)
            )
            if mutation
            else []
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

    def get_spec_extension(self, places):
        extension = {}

        if "Children" not in places:
            extension[f"Children with FormFields"] = "pass"

        if not self.ih.maybe_add_item_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no item pipeline")

        if not self.ih.maybe_add_save_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no save pipeline")

        return extension


def get_form_mutation_or_bvr(widget_spec):
    mutation = None
    editing_bvr = None
    save_pipeline = widget_spec.get_pipeline_by_name("save", recurse=True)
    res = save_pipeline.resources[-1]
    if res.meta.term.tag == "mutation":
        mutation = res.typ
    if res.meta.term.tag == "editing":
        editing_bvr = res.typ
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
