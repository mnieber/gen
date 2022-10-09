from .strip_fk_symbols import strip_fk_symbols
from .strip_generic_symbols import strip_generic_symbols


def convert_type_spec_symbols(type_spec_dict, parent_field=None):
    result = dict()
    for key, value in type_spec_dict.items():
        if key.startswith("__"):
            result[key] = value
            continue

        new_key, new_value = None, None

        parts_through = key.split(" through ")
        foo = parts_through[0]
        bar = parts_through[1] if len(parts_through) > 1 else None

        parts_as = foo.split(" as ")
        foo_var = parts_as[0]
        foo_type = parts_as[1] if len(parts_as) > 1 else None

        if bar:
            parts_as = bar.split(" as ")
            bar_var = parts_as[0]
            bar_type = parts_as[1] if len(parts_as) > 1 else None
        else:
            bar_var, bar_type = None, None

        is_related_fk = isinstance(value, str) and value.split(".")[0] == "RelatedFK"
        if is_related_fk:
            value = dict()

        if isinstance(value, str):
            assert not foo_type
            assert not bar
            foo_var, value_parts = strip_generic_symbols(foo_var)
            new_key, new_value = foo_var, value + (
                "." + " ".join(value_parts) if value_parts else ""
            )
        else:
            new_value = dict(value)
            foo_key, init_parts = strip_fk_symbols(foo_var)

            if foo_type:
                foo_type, more_init_parts = strip_fk_symbols(foo_type)
                init_parts += more_init_parts
                foo_key += " as " + foo_type

            new_value["__init_target__" if bar else "__init__"] = ".".join(init_parts)
            new_key = foo_key

            if is_related_fk:
                assert parent_field
                new_value["__is_reverse_of_related_set__"] = parent_field

            if bar:
                bar_key, init_parts = strip_fk_symbols(bar_var)

                if bar_type:
                    bar_type, more_init_parts = strip_fk_symbols(bar_type)
                    init_parts += more_init_parts
                    bar_key += " as " + bar_type

                new_key += " through " + bar_key
                new_value["__init__"] = ".".join(init_parts)

        if isinstance(new_value, dict):
            new_value = convert_type_spec_symbols(
                new_value, parent_field=new_key.split()[0]
            )

        result[new_key] = new_value

    return result
