from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.template_renderer import render_templates
from moonleap.resources.data_type_spec_store import FK, data_type_spec_store


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


def _graphene_field(field):
    t = field.field_type

    if isinstance(t, FK):
        return f"graphene.ID()"

    if t == "string":
        return f"graphene.String()"

    if t == "date":
        return f"graphene.Date()"

    raise Exception(f"Unknown graphene field type: {t}")


def p_section_graphene_fields(self, item_name):
    result = []
    indent = "    "
    spec = data_type_spec_store.get_spec(item_name)
    for field in _fields(spec):
        graphene_field = _graphene_field(field)
        result.append(indent + f"{field.name_snake} = {graphene_field}")

    return "\n".join(result or [indent + "pass"])


def p_section_exclude(self, item_name):
    spec = data_type_spec_store.get_spec(item_name)
    return ", ".join([x.name_snake for x in _fields(spec) if x.private])
