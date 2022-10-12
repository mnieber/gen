from moonleap.typespec.load_type_specs.strip_generic_symbols import (
    strip_generic_symbols,
)


def apply_type_updates(host, type_spec, updates):
    for field in updates:
        key, parts = strip_generic_symbols(field)

        field_spec = type_spec.get_field_spec_by_key(key)

        if "omit_model" in parts and host in field_spec.has_model:
            field_spec.has_model.remove(host)

        if "omit_api" in parts and host in field_spec.has_api:
            field_spec.has_api.remove(host)

        if "optional" in parts and host not in field_spec.optional:
            field_spec.optional.append(host)

        if "required" in parts and f"required_{host}" not in field_spec.optional:
            field_spec.optional.append(f"required_{host}")
