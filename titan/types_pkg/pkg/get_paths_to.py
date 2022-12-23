from moonleap.utils.fp import uniq
from typespec.api_spec import ApiSpec

# This function returns different paths from type_spec_or_api_spec to
# an fk field of type "type_name", e.g. the path Foo.bar.baz goes
# from the Foo type-spec to the baz field via the bar field.
#
# Why is this needed? Because when we reorder a list of items in the frontend,
# then for performance reasons we would like to immediately apply the same
# reordering to all data-structures in the frontend that have a similar list.
# E.g. when we reorder todolist.todos, then any data-structure that has a
# todolist.todos field should also be reordered.


def get_paths_to(type_name, type_spec_or_api_spec, base_path, skip=None):
    if skip is None:
        skip = []

    is_api_spec = isinstance(type_spec_or_api_spec, ApiSpec)
    type_spec = type_spec_or_api_spec if not is_api_spec else None
    api_spec = type_spec_or_api_spec if is_api_spec else None

    new_skip = skip
    if type_spec:
        if type_spec.type_name in skip:
            return []
        else:
            new_skip = skip + [type_spec.type_name]

    paths = []
    infix = "." if base_path else ""

    field_specs = (
        api_spec.get_outputs(["fk", "relatedSet"])
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
