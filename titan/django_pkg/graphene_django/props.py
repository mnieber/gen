from moonleap.render.add_output_filenames import add_output_filenames
from moonleap.render.template_renderer import render_templates
from moonleap.resources.data_type_spec_store import FK, data_type_spec_store
from moonleap.utils.case import upper0
from moonleap.utils.inflect import plural
from moonleap.utils.magic_replace import magic_replace


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


def _default_value(field, item_name):
    t = field.field_type

    if isinstance(t, FK):
        return f"{field.name_snake}.id"

    if t == "string":
        return r'"foo"'

    if t == "bool":
        return r"True"

    if t == "email":
        return r"email@email.com"

    if t == "date":
        return r'"01-02-2003"'

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name}")


def _graphene_field(field, item_name):
    t = field.field_type

    if isinstance(t, FK):
        return r"graphene.ID()"

    if t == "string":
        return r"graphene.String()"

    if t == "bool":
        return r"graphene.Boolean()"

    if t == "email":
        return r"graphene.String()"

    if t == "date":
        return r"graphene.types.datetime.Date()"

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name}")


def _add_mutation_fields(fields, result):
    for field in fields:
        if field.field_type == "bool":
            result.append(
                f'          {field.name}: {{"true" if {field.name_snake} else "false"}},'
            )
        else:
            result.append(f'          {field.name}: "{{{field.name_snake}}}",')


class Sections:
    def __init__(self, res):
        self.res = res

    def graphene_fields(self, item_name):
        result = []
        indent = "    "
        spec = data_type_spec_store.get_spec(item_name)
        for field in _fields(spec):
            graphene_field = _graphene_field(field, item_name)
            result.append(indent + f"{field.name_snake} = {graphene_field}")

        return "\n".join(result or [indent + "pass"])

    def exclude(self, item_name):
        spec = data_type_spec_store.get_spec(item_name)

        return ", ".join([f'"{x.name_snake}"' for x in _fields(spec) if x.private])

    def mutation_fields(self, module):
        result = []
        indent = "    "

        for form in module.forms:
            result.append(
                indent + f"{form.item_name_snake} = {upper0(form.item_name)}.Field()"
            )

        for item in module.items_received:
            result.append(
                indent
                + f"post_{item.item_name_snake} = Post{upper0(item.item_name)}.Field()"
            )

        return "\n".join(result or [indent + "pass"])

    def query_base_types(self, module):
        result = []

        for item_list in module.item_lists_provided:
            result.append(f"{upper0(plural(item_list.item_name))}Query, ")

        return "".join(result + (["graphene.ObjectType"] if result else []))

    def mutation_base_types(self, module):
        return "graphene.ObjectType" if (module.forms or module.items_received) else ""

    def form_values(self, item_name):
        result = []
        indent = " " * 16
        spec = data_type_spec_store.get_spec(item_name)

        for field in spec.fields:
            value = _default_value(field, item_name)
            result.append(f"{indent}{field.name}={value}, ")

        return "\n".join(result)

    def item_list_query(self, item_list):
        result = []

        if True:
            result.append("def create_red_roses_query(self, output_values):")
            result.append('  query = f"""')
            result.append("      query {{")
            result.append("        redRoses {{")
            result.append('          ",\n          ".join(output_values)')
            result.append("        }}")
            result.append("      }}")
            result.append('    """.format()')
            result.append("  return query")

        return magic_replace(
            "\n".join(result),
            [
                ("red_rose", item_list.item_name_snake),
                ("redRose", item_list.item_name),
            ],
        )

    def form_mutation(self, form):
        result = []
        spec = data_type_spec_store.get_spec(form.item_name + "Form")
        fields = [x for x in spec.fields if not x.private]
        args = (", " if fields else "") + ", ".join([x.name_snake for x in fields])

        if True:
            result.append(f"def create_red_rose_mutation(self{args}, output_values):")
            result.append(r'  query = f"""')
            result.append(r"      mutation {{")
            result.append(r"        redRose(")
        _add_mutation_fields(fields, result)
        if True:
            result.append("        ) {{")
            result.append('          {", ".join(output_values)}')
            result.append("        }}")
            result.append("      }}")
            result.append('    """')
            result.append("  return query")

        return magic_replace(
            "\n".join(result),
            [
                ("red_rose", form.item_name_snake),
                ("redRose", form.item_name),
            ],
        )

    def post_item_mutation(self, item):
        result = []
        spec = data_type_spec_store.get_spec(item.item_name)
        fields = [x for x in spec.fields if not x.private]
        args = (", " if fields else "") + ", ".join([x.name_snake for x in fields])

        if True:
            result.append(
                f"def create_post_red_rose_mutation(self{args}, output_values):"
            )
            result.append(r'  query = f"""')
            result.append(r"      mutation {{")
            result.append(r"        postRedRose(")
        _add_mutation_fields(fields, result)
        if True:
            result.append("        ) {{")
            result.append('          {", ".join(output_values)}')
            result.append("        }}")
            result.append("      }}")
            result.append('    """')
            result.append("  return query")

        return magic_replace(
            "\n".join(result),
            [
                ("red_rose", item.item_name_snake),
                ("redRose", item.item_name),
            ],
        )
