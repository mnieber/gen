from ramda import merge

from moonleap.utils import str_to_type_id


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules_by_resource_type_id = {}
        self.is_ittable_by_tag = {}

    def get_update_rules(self, parent_resource_id):
        return self.update_rules_by_resource_type_id.get(parent_resource_id) or {}


config = Config()


def install(module):
    for tag in module.tags:
        config.create_rule_by_tag[tag] = module.create
        config.is_ittable_by_tag[tag] = getattr(module, "is_ittable", False)


def reduce(parent_resource, resource):
    resource_id = (
        resource if isinstance(resource, str) else str_to_type_id(resource.__module__)
    )
    parent_resource_id = (
        parent_resource
        if isinstance(parent_resource, str)
        else str_to_type_id(parent_resource.__module__)
    )

    def wrapped(f):
        config.update_rules_by_resource_type_id.setdefault(parent_resource_id, {})
        config.update_rules_by_resource_type_id[parent_resource_id][resource_id] = f

    return wrapped
