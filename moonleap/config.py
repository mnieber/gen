from ramda import merge

from moonleap.utils import resource_id_from_class


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules_by_resource_type_id = {}
        self.render_function_by_resource_type_id = {}
        self.is_ittable_by_tag = {}

    def get_update_rules(self, resource_id):
        return self.update_rules_by_resource_type_id.get(resource_id) or {}


config = Config()


def install(module):
    for tag in module.tags:
        config.create_rule_by_tag[tag] = module.create
        config.is_ittable_by_tag[tag] = getattr(module, "is_ittable", False)
    config.render_function_by_resource_type_id = merge(
        config.render_function_by_resource_type_id,
        {
            resource_id_from_class(resource): render
            for resource, render in module.render_function_by_resource_type
        },
    )


def reduce(a_resource, b_resource):
    b_resource_id = (
        b_resource
        if isinstance(b_resource, str)
        else resource_id_from_class(b_resource)
    )
    a_resource_id = (
        a_resource
        if isinstance(a_resource, str)
        else resource_id_from_class(a_resource)
    )

    def register(res_id_1, res_id_2, f, is_reversed):
        config.update_rules_by_resource_type_id.setdefault(res_id_1, {})
        config.update_rules_by_resource_type_id[res_id_1][res_id_2] = (f, is_reversed)

    def wrapped(f):
        register(a_resource_id, b_resource_id, f, False)
        register(b_resource_id, a_resource_id, f, True)

    return wrapped
