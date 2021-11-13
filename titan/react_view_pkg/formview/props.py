import ramda as R
from moonleap import u0
from moonleap.utils.chop import chop_postfix
from moonleap.utils.codeblock import CodeBlock
from moonleap.utils.inflect import plural
from titan.api_pkg.pkg.ml_name import ml_form_type_spec_from_item_name
from titan.api_pkg.typeregistry import TypeRegistry
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
from titan.react_pkg.pkg.ts_var import ts_type_from_item_name
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self, named_component):
    url = get_component_base_url(self, self.name)
    return [
        create_component_router_config(self, named_component=named_component, url=url)
    ]


def get_related_field_name(field_spec, string_field_specs):
    relatedFieldName = field_spec.field_type_attrs.get("relatedFieldName")
    if not relatedFieldName:
        stringField = R.head(string_field_specs)
        relatedFieldName = stringField.name if stringField else ""
    return relatedFieldName


def _get_field_name(field_spec, fk_field_specs):
    name = (
        chop_postfix(field_spec.name, "Id")
        if field_spec in fk_field_specs
        else field_spec.name
    )
    return name


def get_context(form_view):
    _ = lambda: None
    _.type_spec = ml_form_type_spec_from_item_name(form_view.item_posted.item_name)
    _.field_specs = [x for x in _.type_spec.field_specs if x.name != "id"]
    _.fk_field_specs = [x for x in _.type_spec.get_field_specs(["uuid"]) if x.target]
    _.graphql_api = ml_graphql_api(ml_react_app(form_view))
    _.type_reg = TypeRegistry(_.graphql_api)

    _.mutation = R.head(form_view.item_posted.poster_mutations)
    _.postmethod = _.mutation.name

    class Sections:
        def form_imports(self):
            root = CodeBlock(style="typescript", level=0)
            for field_spec in _.fk_field_specs:
                item_name = field_spec.target
                item_list = _.type_reg.get_item_list_by_name(item_name)
                module = item_list.provider_react_store.module
                root.abc(
                    f"import {{ {ts_type_from_item_name(item_name)} }} "
                    + f"from '{module.module_path}/types'"
                )
            return root.result

        def form_default_props(self):
            root = CodeBlock(style="typescript", level=0)
            for field_spec in _.fk_field_specs:
                root.abc(
                    f"  {plural(field_spec.target)}: "
                    + f"{ts_type_from_item_name(field_spec.target)}[]"
                )
            return root.result

        def initial_form_values(self):
            root = CodeBlock(style="typescript", level=0)

            for field_spec in _.field_specs:
                name = _get_field_name(field_spec, _.fk_field_specs)
                value = (
                    "''"
                    if field_spec.field_type
                    in (
                        "slug",
                        "string",
                    )
                    else "false"
                    if field_spec.field_type in ("boolean",)
                    else "null"
                )
                root.abc(f"{name}: {value},")
            return root.result

        def form_field(self, field_spec):
            name = _get_field_name(field_spec, _.fk_field_specs)
            item_name = field_spec.target
            root = CodeBlock(style="typescript", level=2)

            buttons = ""
            label = name
            if field_spec.field_type in ("slug",):
                related_field_name = get_related_field_name(
                    field_spec, _.type_spec.get_field_specs(["string"])
                )
                buttons = (
                    r" buttons={["
                    + f'<UpdateSlugButton key="1" relatedFieldName="{related_field_name}" />'
                    + r"]}"
                )
            elif field_spec.field_type in ("uuid",) and item_name:
                label = chop_postfix(field_spec.name, "Id")

            root.abc(f'<Field fieldName="{name}" label="{u0(label)}"{buttons}>')
            if field_spec.field_type in ("string", "url"):
                root.abc(r"  <TextField controlled={true} />")
            elif field_spec.field_type in ("slug",):
                root.abc(r"  <SlugField />")
            elif field_spec.field_type in ("uuid",) and item_name:
                display_field = field_spec.target_type_spec.display_item_by
                root.abc(r"  <ValuePickerField")
                root.abc(r"    isCreatable={false}")
                root.abc(r"    isMulti={false}")
                root.abc(f"    pickableValues={{props.{plural(item_name)}}}")
                root.abc(f"    labelFromValue={{(x: any) => x.{display_field}}}")
                root.abc(r"  />")
            elif field_spec.field_type in ("boolean",):
                root.abc(r"  <ControlledCheckbox />")
            else:
                return ""

            root.abc(r"</Field>")
            return root.result

        def validate_form(self):
            root = CodeBlock(style="typescript", level=2)
            for field_spec in _.field_specs:
                name = _get_field_name(field_spec, _.fk_field_specs)
                if field_spec.required:
                    root.abc(f"if (R.isNil(values.{name})) {{")
                    root.abc(f"  setError('{name}', 'This field is required')")
                    root.abc(r"}")
            return root.result

        def post_form(self):
            args = [r"{ ...values"]
            for field_spec in _.fk_field_specs:
                chopped_name = chop_postfix(field_spec.name, "Id")
                args.append(f"{field_spec.name}: values.{chopped_name}.id")
                args.append(f"{chopped_name}: undefined")
            args.append(r"} as any")
            root = CodeBlock(style="typescript", level=2)
            root.IxI(_.postmethod, args, "")
            return root.result

    return dict(sections=Sections(), _=_)
