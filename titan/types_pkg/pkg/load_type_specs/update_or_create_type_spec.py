from titan.types_pkg.pkg.form_type_spec_from_data_type_spec import (
    form_type_spec_from_data_type_spec,
)
from titan.types_pkg.pkg.type_spec import TypeSpec

from .add_host_to_type_spec import add_host_to_type_spec


def update_or_create_type_spec(
    host, type_reg, type_name, parts, module_name, parent_type_spec
):
    type_spec = type_reg.get(type_name, default=None)
    if not type_spec:
        if type_name.endswith("Form"):
            data_type_spec = type_reg.get(type_name[:-4])
            if data_type_spec:
                type_spec = form_type_spec_from_data_type_spec(
                    data_type_spec, type_name
                )
                if host != "server":
                    add_host_to_type_spec(host, type_spec)
        if not type_spec:
            type_spec = TypeSpec(type_name=type_name, field_specs=[])
        type_reg.setdefault(type_name, type_spec)

    # Update module name
    if module_name:
        if type_spec.module_name and type_spec.module_name != module_name:
            raise Exception(
                f"Type {type_spec.type_name} is defined in two modules: "
                + f"{type_spec.module_name} and {module_name}"
            )
        type_spec.module_name = module_name

    if "is_sorted" in parts:
        type_spec.is_sorted = True

    if "entity" in parts:
        type_spec.is_entity = True

    if "extract_gql_fields" in parts:
        type_spec.extract_gql_fields = True

    # Register parent
    if parent_type_spec:
        type_reg.register_parent_child(parent_type_spec.type_name, type_spec.type_name)

    return type_spec
