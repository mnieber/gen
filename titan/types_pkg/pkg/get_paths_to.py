from moonleap.utils.fp import uniq
from titan.api_pkg.pkg.api_spec import ApiSpec


def get_paths_to(type_name, type_spec, base_path, skip=None):
    if skip is None:
        skip = []

    is_api_spec = isinstance(type_spec, ApiSpec)
    new_skip = skip
    if not is_api_spec:
        if type_spec.type_name in skip:
            return []
        else:
            new_skip = skip + [type_spec.type_name]

    paths = []
    infix = "." if base_path else ""

    field_specs = (
        type_spec.get_outputs(["fk", "relatedSet"])
        if is_api_spec
        else type_spec.get_field_specs(["fk", "relatedSet"])
    )

    for field_spec in field_specs:
        if field_spec.field_type == "fk":
            new_path = base_path + infix + field_spec.name
        else:
            new_path = base_path + infix + field_spec.name + ".*"

        if field_spec.target == type_name:
            paths.append(new_path)
        else:
            more_paths = get_paths_to(
                type_name, field_spec.target_type_spec, new_path, new_skip
            )
            paths.extend(more_paths)

    return uniq(paths)
