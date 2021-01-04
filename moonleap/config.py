from pathlib import Path

from ramda import merge

from moonleap.utils import resource_id_from_class


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules_by_resource_type_id = {}
        self.templates_by_resource_type_id = {}
        self.is_ittable_by_tag = {}

    def get_update_rules(self, resource_id):
        return self.update_rules_by_resource_type_id.get(resource_id) or {}


config = Config()


def install(module):
    for tag in module.tags:
        config.create_rule_by_tag[tag] = module.create
        config.is_ittable_by_tag[tag] = getattr(module, "is_ittable", False)

    config.templates_by_resource_type_id = merge(
        config.templates_by_resource_type_id,
        {
            resource_id_from_class(resource): str(
                Path(module.__file__).parent / templates
            )
            for resource, templates in getattr(module, "templates_by_resource_type", [])
        },
    )


def derive(resource):
    resource_id = get_type_id(resource)

    def wrapped(f):
        config.update_rules_by_resource_type_id.setdefault(resource_id, [])
        config.update_rules_by_resource_type_id[resource_id].append(f)

    return wrapped
