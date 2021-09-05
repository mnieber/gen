from moonleap.resources.data_type_spec_store import FK, data_type_spec_store
from moonleap.utils.magic_replace import magic_replace


def _default_value(field, item_name):
    t = field.field_type

    if isinstance(t, FK):
        return f"{field.name_snake}.id"

    if t == "bool":
        return r"True"

    if t == "date":
        return r'"01-02-2003"'

    if t == "email":
        return r"email@email.com"

    if t == "slug":
        return r"foo-bar"

    if t == "string":
        return r'"foo"'

    if t == "url":
        return r'"https://foo.bar.com"'

    raise Exception(f"Unknown graphene field type: {t} in spec for {item_name}")


def _add_mutation_fields(fields, result):
    for field in fields:
        if field.field_type == "bool":
            result.append(
                f'          {field.name}: {{"true" if {field.name_snake} else "false"}},'
            )
        else:
            result.append(f'          {field.name}: "{{{field.name_snake}}}",')


class EndPointSectionsMixin:
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
        spec = data_type_spec_store.get_spec(form.data_type_name)
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

    def form_values(self, item_name):
        result = []
        indent = " " * 16
        spec = data_type_spec_store.get_spec(item_name)

        for field in spec.fields:
            value = _default_value(field, item_name)
            result.append(f"{indent}{field.name}={value}, ")

        return "\n".join(result)
