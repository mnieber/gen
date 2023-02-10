import typing as T
from dataclasses import dataclass, field

from jdoc.titan.widget_reg import WidgetSpec
from titan.api_pkg.apiregistry.resources import Mutation
from titan.react_view_pkg.behavior.resources import EditingBehavior
from titan.typespec.api_spec import ApiSpec
from titan.typespec.field_spec import FieldSpec


@dataclass
class FormField:
    name: str
    prefix: str = ""
    through: T.Optional[str] = None
    field_spec: T.Optional[FieldSpec] = None

    @property
    def dot_name(self):
        return f"{self.prefix}{self.through or self.name}"


@dataclass
class FormData:
    fields: T.List[FormField] = field(default_factory=list)
    mutation: T.Optional[Mutation] = None
    editing_bvr: T.Optional[EditingBehavior] = None


def _get_form_fields(
    widget_spec, form_field_specs, scalar_field_specs, default_field_datas
):
    field_datas_by_form_name = widget_spec.src_dict.get(
        "__fields__", default_field_datas
    )
    if field_datas_by_form_name is None:
        return None

    fields = []
    for form_name, field_datas in field_datas_by_form_name.items():
        clean_form_name = form_name.rstrip("~")
        prefix = "" if clean_form_name == "." else clean_form_name + "."
        for field_data in field_datas:
            if isinstance(field_data, dict):
                field_name = field_data["name"]
                through = field_data["through"]
            else:
                field_name = field_data
                through = None
            field_spec = _get_field_spec(
                scalar_field_specs, form_field_specs, prefix + field_name
            )

            form_field = FormField(
                name=field_name,
                prefix=prefix,
                through=through,
                field_spec=field_spec,
            )
            fields.append(form_field)

    return fields


def _get_field_spec(scalar_field_specs, form_field_specs, field_name: str):
    if "." in field_name:
        for form_field_spec in form_field_specs:
            for scalar_field_spec in _form_fields(form_field_spec):
                form_field_name = f"{form_field_spec.name}.{scalar_field_spec.name}"
                if field_name == form_field_name:
                    return scalar_field_spec
    else:
        for scalar_field_spec in scalar_field_specs:
            if field_name == scalar_field_spec.name:
                return scalar_field_spec

    return None


def _form_fields(form_field_spec):
    return [
        x
        for x in form_field_spec.target_type_spec.get_field_specs()
        if "client" in x.has_model
    ]


def widget_spec_get_form_data(widget_spec, recurse=False):
    form_field_specs = []
    scalar_field_specs = []
    mutation, editing_bvr = _get_mutation_and_editing_bvr(widget_spec)
    if mutation:
        scalar_field_specs = [
            x for x in mutation.api_spec.get_inputs() if x.field_type != "form"
        ]
        form_field_specs = mutation.api_spec.get_inputs(["form"])

    default_field_datas = {}
    for form_field_spec in form_field_specs:
        default_field_datas[form_field_spec.name] = [
            x.name for x in _form_fields(form_field_spec)
        ]

    ws = widget_spec
    while ws:
        fields = _get_form_fields(
            ws,
            form_field_specs,
            scalar_field_specs,
            default_field_datas=None if ws.parent else default_field_datas,
        )

        if fields != None:
            return FormData(
                fields=fields,
                mutation=mutation,
                editing_bvr=editing_bvr,
            )
        ws = ws.parent if recurse else None
    return None


def _get_mutation_and_editing_bvr(widget_spec):
    mutation = None
    editing_bvr = None
    save_pipeline = widget_spec.get_pipeline_by_name("save", recurse=True)
    res = save_pipeline.resources[-1]
    if res.meta.term.tag == "mutation":
        mutation = res
    if res.meta.term.tag == "editing":
        editing_bvr = res.typ
        mutation = editing_bvr.mutation
    return mutation, editing_bvr
