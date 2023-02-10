from pathlib import Path

import ramda as R

from moonleap import get_tpl, u0
from titan.react_view_pkg.pkg.add_tpl_to_builder import add_tpl_to_builder
from titan.react_view_pkg.pkg.builder import Builder
from titan.types_pkg.typeregistry import get_type_reg


class FormStateProviderBuilder(Builder):
    type = "FormStateProvider"

    def __post_init__(self):
        self.tpl = None

    def build(self):
        self.add_div_open()
        self.add_body()
        self.add_div_close()

    def add_div_open(self):
        context = self.get_context()
        self.tpl = get_tpl(Path(__file__).parent / "tpl.tsx.j2", context)
        self.output.add(lines=[self.tpl.get_section("div_open")])

    def add_div_close(self):
        assert self.tpl
        self.output.add(lines=[self.tpl.get_section("div_close")])

    def add_body(self):
        from titan.react_view_pkg.pkg.build_widget_spec import build_widget_spec

        children_ws = self.widget_spec.get_place("Children")
        children_build_output = build_widget_spec(children_ws)

        assert self.tpl
        add_tpl_to_builder(self.tpl, self)
        self.output.add(lines=[*children_build_output.lines])
        self.output.graft(children_build_output)

    def get_context(self):
        # We expect the widget_spec to have a "save" pipeline
        form_data = self.widget_spec.get_form_data(recurse=True)
        fields = form_data.fields

        item_name = self.ih.working_item_name
        assert item_name

        return dict(
            item_name=item_name,
            type_spec=get_type_reg().get(u0(item_name) + "Form"),
            mutation=form_data.mutation,
            editing_bvr=form_data.editing_bvr,
            location_state=R.head(
                [
                    x
                    for x in self.widget_spec.root.named_default_props
                    if _is_location_state(x)
                ]
            ),
            fields=fields,
            uuid_fields=[
                x
                for x in fields
                if x.field_spec.field_type == "uuid" and x.field_spec.target
            ],
            through_fields=[x for x in fields if x.through],
            validated_fields=_get_validated_fields(fields),
            get_initial_value=_get_initial_value,
        )

    def get_spec_extension(self, places):
        extension = {}

        if "Children" not in places:
            extension[f"Children with FormFields"] = "pass"

        if not self.ih.maybe_add_item_pipeline_to_spec_extension(
            "component:props", extension
        ):
            raise Exception("FormStateProviderBuilder: no item pipeline")

        if not self.ih.maybe_add_save_pipeline_to_spec_extension(extension):
            raise Exception("FormStateProviderBuilder: no save pipeline")

        return extension


def _get_initial_value(form_field):
    if form_field.field_spec.field_type == "boolean":
        return "false"
    elif form_field.field_spec.field_type == "uuid":
        return "createUUID().hex"
    return "null"


def _get_validated_fields(fields):
    return [
        field
        for field in fields
        if (
            not field.field_spec.is_optional("client")
            and not field.field_spec.field_type == "boolean"
        )
    ]


def _is_location_state(named_res):
    term = named_res.meta.term
    return term.tag == "state" and term.data == "location"
