from moonleap.typespec.load_type_specs.strip_generic_symbols import (
    strip_generic_symbols,
)
from moonleap.utils.fp import append_uniq


def apply_type_updates(host, type_spec, updates):
    for field in updates:
        key, parts = strip_generic_symbols(field)

        field_spec = type_spec.get_field_spec_by_key(key)
        if not field_spec:
            raise Exception(f"Cannot update type {type_spec}. Field {key} not found.")

        if "omit_model" in parts and host in field_spec.has_model:
            field_spec.has_model.remove(host)

        if "omit_api" in parts and host in field_spec.has_api:
            field_spec.has_api.remove(host)

        if "optional" in parts and host not in field_spec.optional:
            append_uniq(field_spec.optional, host)

        if "required":
            append_uniq(field_spec.optional, f"required_{host}")
