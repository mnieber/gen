from moonleap import u0


def find_module_that_provides_item_list(django_app, item_name):
    for module in django_app.modules:
        for item_list in module.item_lists_provided:
            if item_list.item_name == item_name:
                return module
    return None


def endpoint_imports(django_app, item_names, field_spec):
    result = []

    if field_spec.field_type in ("fk", "related_set", "form"):
        item_name = field_spec.field_type_attrs["target"]
        if item_name in item_names:
            return result
        item_names.add(item_name)

        tn_graphene = field_spec.fk_type_spec.tn_graphene
        result.append(
            f"from api.types.{tn_graphene.lower()} " + f"import {tn_graphene}"
        )

        module = find_module_that_provides_item_list(django_app, item_name)
        if module:
            result.append(f"from {module.name}.models import {u0(item_name)}")

    return result
