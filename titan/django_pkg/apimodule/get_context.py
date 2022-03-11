from titan.django_pkg.graphene_django.utils import find_module_that_provides_item_list


def get_context(api_module):
    _ = lambda: None
    _.item_types = list()
    for item_type in api_module.graphql_api.type_reg.item_types:
        if find_module_that_provides_item_list(
            api_module.django_app, item_type.name, raise_if_not_found=False
        ):
            _.item_types.append(item_type)

    _.item_form_types = list()
    for item_type in api_module.graphql_api.item_types_posted:
        if find_module_that_provides_item_list(
            api_module.django_app, item_type.name, raise_if_not_found=False
        ):
            _.item_form_types.append(item_type)

    class Sections:
        pass

    return dict(sections=Sections(), _=_)
