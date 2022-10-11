from moonleap.typespec.load_type_specs.get_foo_bar import get_foo_bar
from moonleap.utils.case import u0

from .strip_fk_symbols import strip_fk_symbols
from .strip_generic_symbols import strip_generic_symbols


def strip_symbols(type_spec_dict, parent_field=None):
    if parent_field is None:
        type_spec_dict["__type_name__"] = "root"

    result = dict()
    for key, value in type_spec_dict.items():
        if key.startswith("__"):
            result[key] = value
            continue

        new_key, new_value = None, None

        is_related_fk = isinstance(value, str) and value.split(".")[0] == "RelatedFk"
        if is_related_fk:
            assert parent_field
            value = {"__is_reverse_of_related_set__": parent_field}

        if isinstance(value, str):
            new_key, value_parts = strip_generic_symbols(key)
            if "derived" in value_parts:
                new_key += "^"
            new_value = value + ("." + ".".join(value_parts) if value_parts else "")
        else:
            new_value = dict(value)
            foo, bar = get_foo_bar(key)

            # The user supplied models.yaml may already have the __init__ key
            init_parts = (
                new_value["__init__"].split(".") if "__init__" in new_value else []
            )
            init_target_parts = (
                new_value["__init_target__"].split(".")
                if "__init_target__" in new_value
                else []
            )
            foo.var_type, more_init_parts = strip_fk_symbols(foo.var_type)

            if bar:
                init_target_parts += more_init_parts
            else:
                init_parts += more_init_parts

            new_key = foo.var_type
            if foo.var:
                foo.var, more_init_parts = strip_fk_symbols(foo.var)
                if bar:
                    init_target_parts += more_init_parts
                else:
                    init_parts += more_init_parts
                new_key = foo.var + " as " + new_key

            if bar:
                bar.var_type, more_init_parts = strip_fk_symbols(bar.var_type)
                init_parts += more_init_parts
                bar_key = bar.var_type

                if bar.var:
                    bar.var, more_init_parts = strip_fk_symbols(bar.var)
                    init_parts += more_init_parts
                    bar_key = bar.var + " as " + bar.var_type

                new_key += " through " + bar_key

            new_value["__init__"] = ".".join(init_parts)
            if bar:
                new_value["__init_target__"] = ".".join(init_target_parts)

            #
            # Use recursion to convert child type specs
            #
            new_value["__type_name__"] = u0(
                bar.var_type if bar else foo.var_type
            ).removesuffix("Set")

            field_name = new_key.split()[0]
            new_value = strip_symbols(
                new_value,
                parent_field=type_spec_dict["__type_name__"] + "." + field_name,
            )

        result[new_key] = new_value

    return result
