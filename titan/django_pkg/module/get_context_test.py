from moonleap.utils.case import sn
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def _get_faker_value(field_spec):
    if field_spec.field_type == "boolean":
        return f"f.boolean()"

    if field_spec.field_type in ("string", "slug"):
        return f"f.word()"

    if field_spec.field_type == "uuid":
        return f"f.uuid4()"

    raise Exception(f"Cannot deduce faker function for {field_spec.field_type}")


def get_context_test(module):
    class Sections:
        def create_random_args(self, item_name):
            type_spec = ml_type_spec_from_item_name(item_name)
            fk_field_names = [
                f"{sn(field_spec.name + 'Id')}"
                for field_spec in type_spec.get_field_specs(["fk"])
                if not field_spec.through
            ]
            return ", ".join(fk_field_names)

        def create_random_body(self, item_name, snake_args):
            type_spec = ml_type_spec_from_item_name(item_name)
            args = []
            transform_name = sn if snake_args else lambda x: x
            for field_spec in type_spec.field_specs:
                if field_spec.field_type == "fk":
                    if not field_spec.through:
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

    return dict(sections=Sections())
