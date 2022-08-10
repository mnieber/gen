from moonleap.utils.case import sn


def _get_faker_value(field_spec):
    if field_spec.field_type == "boolean":
        return f"f.boolean()"

    if field_spec.field_type == "int":
        return f"f.random_int()"

    if field_spec.field_type == "float":
        return f"f.random_number(digits=2)"

    if field_spec.field_type in ("string", "slug"):
        return f"f.word()"

    if field_spec.field_type == "uuid":
        return f"f.uuid4()"

    if field_spec.field_type == "date":
        return f"f.date()"

    if field_spec.field_type == "json":
        return "{}"

    if field_spec.field_type == "url":
        return "'www.example.com'"

    raise Exception(f"Cannot deduce faker function for {field_spec.field_type}")


def get_helpers(_):
    class Helpers:
        def create_random_args(self, item_list):
            fk_field_names = [
                f"{sn(field_spec.name + 'Id')}"
                for field_spec in item_list.type_spec.get_field_specs(["fk"])
            ]
            return ", ".join(fk_field_names)

        def create_random_body(self, item_list, snake_args):
            args = []
            transform_name = sn if snake_args else lambda x: x
            for field_spec in item_list.type_spec.field_specs:
                if field_spec.field_type == "fk":
                    args.append(
                        f"{transform_name(field_spec.name + 'Id')}={sn(field_spec.name + 'Id')}"
                    )
                elif field_spec.field_type == "relatedSet":
                    pass
                else:
                    args.append(
                        f"{transform_name(field_spec.name)}={_get_faker_value(field_spec)}"
                    )
            return ",\n      ".join(args)

    return Helpers()
