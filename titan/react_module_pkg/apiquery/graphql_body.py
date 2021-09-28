import os

from moonleap import u0
from moonleap.resources.type_spec_store import type_spec_store


def graphql_body(type_spec=None, indent=0, skip=None):
    is_top_level = not skip

    if skip is None:
        skip = [type_spec.type_name]

    if type_spec is None:
        type_spec = _.query.outputs_type_spec

    result = []
    for spec_field in type_spec.field_specs:
        if spec_field.field_type in ("fk", "related_set"):
            fk_type_name = u0(spec_field.field_type_attrs["target"])
            if fk_type_name not in skip:
                fk_type_spec = type_spec_store().get(fk_type_name)
                include_field_name = (
                    spec_field.field_type in ("fk", "related_set") and not is_top_level
                )
                if include_field_name:
                    result.append(f"{spec_field.name} {{")
                    indent += 2
                result.extend(
                    graphql_body(
                        fk_type_spec,
                        indent,
                        skip + [fk_type_name],
                    )
                )
                if include_field_name:
                    indent -= 2
                    result.append(f"}}")
        else:
            result.append(f"{spec_field.name}")

    if is_top_level:
        return " " * 10 + (os.linesep + (" " * 10)).join(result)
    else:
        return [(" " * indent) + x for x in result]
