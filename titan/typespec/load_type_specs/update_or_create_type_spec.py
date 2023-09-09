from moonleap import u0
from moonleap.utils.fp import append_uniq
from titan.typespec.type_spec import TypeSpec


def update_or_create_type_spec(type_reg, fk, value):
    type_name = fk.var_type
    parts = fk.parts

    type_spec = type_reg.get(type_name)
    if not type_spec:
        type_spec = TypeSpec(type_name=type_name, field_specs=[])
        type_reg.setdefault(type_name, type_spec)

    module_name = value.get("__module__") or fk.module_name
    if module_name:
        if type_spec.module_name and type_spec.module_name != module_name:
            raise Exception(
                f"Conflicting module names for {type_spec.type_name}: "
                f"{type_spec.module_name} and {module_name}"
            )
        type_spec.module_name = module_name

    base_type_name = u0(value["__base_type__"]) if "__base_type__" in value else None
    if not type_spec.base_type_name:
        type_spec.base_type_name = base_type_name

    if "is_sorted" in parts:
        type_spec.is_sorted = True
        value["sortPos"] = "Int = 0"
        api_spec = value.setdefault("__api__", {})
        deleted_fields = api_spec.setdefault("__delete__", [])
        append_uniq(deleted_fields, "sortPos")

    if "entity" in parts:
        type_spec.is_entity = True
        value["id"] = "Id,primary_key"

    if "no_api" in parts:
        type_spec.no_api = True

    return type_spec
