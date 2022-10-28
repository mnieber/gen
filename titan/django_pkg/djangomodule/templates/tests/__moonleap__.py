from moonleap.utils.case import sn

field_name_block_list = ["sortPos", "id"]


def _get_faker_value(field_spec):
    if field_spec.field_type == "boolean":
        return f"f.boolean()"

    if field_spec.field_type == "int":
        return f"f.random_int()"

    if field_spec.field_type == "float":
        return f"f.random_number(digits=2)"

    if field_spec.field_type in ("string", "text", "slug"):
        return f"f.word()"

    if field_spec.field_type == "string[]":
        return f"[f.word(), f.word()]"

    if field_spec.field_type == "int[]":
        return f"[f.random_int(), f.random_int()]"

    if field_spec.field_type == "uuid":
        return f"f.uuid4()"

    if field_spec.field_type == "uuid[]":
        return f"[f.uuid4(), f.uuid4()]"

    if field_spec.field_type == "date":
        return f"f.date()"

    if field_spec.field_type == "json":
        return "{}"

    if field_spec.field_type == "image":
        return '"image.jpg"'

    if field_spec.field_type == "markdown":
        return '"# " + f.word()'

    if field_spec.field_type == "url":
        return "'www.example.com'"

    raise Exception(f"Cannot deduce faker function for {field_spec.field_type}")


def get_helpers(_):
    class Helpers:
        def create_random_args(self, django_model):
            type_spec = django_model.type_spec
            fk_field_names = [
                f"{sn(field_spec.name + 'Id')}"
                for field_spec in type_spec.get_field_specs(["fk"])
                if "server" in field_spec.has_model
            ]
            return ", ".join(fk_field_names)

        def create_random_body(self, django_model, snake_args):
            args = []
            transform_name = sn if snake_args else lambda x: x
            type_spec = django_model.type_spec
            for field_spec in [
                x for x in type_spec.get_field_specs() if "server" in x.has_model
            ]:
                if field_spec.field_type == "fk":
                    args.append(
                        f"{transform_name(field_spec.name + 'Id')}={sn(field_spec.name + 'Id')}"
                    )
                elif field_spec.field_type == "relatedSet":
                    pass
                elif field_spec.name in field_name_block_list:
                    pass
                else:
                    args.append(
                        f"{transform_name(field_spec.name)}={_get_faker_value(field_spec)}"
                    )
            return ",\n      ".join(args)

    return Helpers()
