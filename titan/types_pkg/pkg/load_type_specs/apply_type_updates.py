from moonleap.utils.fp import append_uniq

from .split_raw_key import split_raw_key


def apply_type_updates(host, type_spec, updates):
    for field in updates:
        key, symbols, parts = split_raw_key(field)

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
