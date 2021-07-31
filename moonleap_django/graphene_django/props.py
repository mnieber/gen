from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.template_renderer import render_templates
from moonleap.resources.data_type_spec_store import FK, data_type_spec_store
from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural


def render(self, output_root_dir, template_renderer):
    all_output_filenames = []

    for module in self.service.django_app.modules:
        if module.item_types or module.forms:
            add_output_filenames(
                all_output_filenames,
                render_templates(__file__, "templates_module", graphene=self)(
                    module, output_root_dir, template_renderer
                ),
            )
    return all_output_filenames


def _fields(spec):
    return [x for x in spec.fields if x.name_snake != "id"]


def _default_value(field, item_name_camel):
    t = field.field_type

    if isinstance(t, FK):
        return f"{field.name_snake}_id"

    if t == "string":
        return f'"foo"'

    if t == "bool":
        return f"true or false"

    if t == "date":
        return f'"01-02-2003"'

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name_camel}")


def _graphene_field(field, item_name_camel):
    t = field.field_type

    if isinstance(t, FK):
        return f"graphene.ID()"

    if t == "string":
        return f"graphene.String()"

    if t == "bool":
        return f"graphene.Boolean()"

    if t == "date":
        return f"graphene.types.datetime.Date()"

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name_camel}")


def p_section_graphene_fields(self, item_name_camel):
    result = []
    indent = "    "
    spec = data_type_spec_store.get_spec(item_name_camel)
    for field in _fields(spec):
        graphene_field = _graphene_field(field, item_name_camel)
        result.append(indent + f"{field.name_snake} = {graphene_field}")

    return "\n".join(result or [indent + "pass"])


def p_section_exclude(self, item_name_camel):
    spec = data_type_spec_store.get_spec(item_name_camel)
    return ", ".join([f'"{x.name_snake}"' for x in _fields(spec) if x.private])


def p_section_mutation_fields(self, module):
    result = []
    indent = "    "

    for form in module.forms:
        result.append(
            indent + f"{form.item_name_snake} = {upper0(form.item_name_camel)}.Field()"
        )

    for item in module.items_received:
        result.append(
            indent
            + f"post_{item.item_name_snake} = Post{upper0(item.item_name_camel)}.Field()"
        )

    return "\n".join(result or [indent + "pass"])


def p_section_query_base_types(self, module):
    result = []

    for item_list in module.item_lists_provided:
        result.append(f"{upper0(plural(item_list.item_name_camel))}Query, ")

    return "".join(result)


def p_section_form_arguments(self, item_name_camel):
    result = []
    indent = " " * 20
    spec = data_type_spec_store.get_spec(item_name_camel)

    for field in spec.fields:
        quote = '"' if field.field_type == "string" else ""
        result.append(
            f"{indent}{field.name_camel}: {quote}{{{field.name_camel}}}{quote}, "
        )

    return "\n".join(result)


def p_section_form_values(self, item_name_camel):
    result = []
    indent = " " * 16
    spec = data_type_spec_store.get_spec(item_name_camel)

    for field in spec.fields:
        value = _default_value(field, item_name_camel)
        result.append(f"{indent}{field.name_camel}={value}, ")

    return "\n".join(result)


def p_section_item_fields(self, item_name_camel):
    result = []
    indent = " " * 16
    spec = data_type_spec_store.get_spec(item_name_camel)

    for field in spec.fields:
        if field.private:
            continue
        result.append(indent + field.name_camel + ", ")

    return "\n".join(result)
