from ramda import merge

from moonleap.utils import resource_id_from_class


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


def reduce(parent_resource, resource, delay=False):
    resource_id = (
        resource if isinstance(resource, str) else resource_id_from_class(resource)
    )
    parent_resource_id = (
        parent_resource
        if isinstance(parent_resource, str)
        else resource_id_from_class(parent_resource)
    )

    def wrapped(f):
        config.update_rules_by_resource_type_id.setdefault(parent_resource_id, {})
        config.update_rules_by_resource_type_id[parent_resource_id][resource_id] = (
            f,
            delay,
        )

    return wrapped
