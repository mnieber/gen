from pathlib import Path

from ramda import merge


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.derive_rules_by_resource_type = {}
        self.is_ittable_by_tag = {}
        self.meta_by_resource_type = {}

    def get_derive_rules(self, resource_type):
        return self.derive_rules_by_resource_type.get(resource_type) or {}


config = Config()


def install(module):
    config.is_ittable_by_tag[tag] = getattr(module, "is_ittable", False)

    for resource_type, class_props in module.meta.items():
        class_meta = self.meta_by_resource_type.setdefault(resource_type, {})

        class_meta['templates'] = str(Path(module.__file__).parent / class_props['templates'])

        for prop_name, parent_resource_type in class_meta.get('parents', {}).items():
            parent_types = class_meta.setdefault('parent_types', [])
            is_list = isinstance(parent_resource_type, list)
            parent_type = parent_resource_type[0] if is_list else parent_resource_type
            if parent_type not in parent_types:
                parent_types.append(parent_type)

            resource_type.setattr(prop_name) = (
                lambda self: self.parents(parent_resource_type)
                if is_list else
                lambda self: self.parent(parent_resource_type)
            )

        for prop_name, child_resource_type in class_meta.get('children', {}).items():
            child_types = class_meta.setdefault('child_types', [])
            is_list = isinstance(child_resource_type, list)
            child_type = child_resource_type[0] if is_list else child_resource_type
            if child_type not in child_types:
                child_types.append(child_type)

            resource_type.setattr(prop_name) = (
                lambda self: self.childten(child_resource_type)
                if is_list else
                lambda self: self.child(child_resource_type)
            )


def derive(resource_type):
    def wrapped(f):
        config.derive_rules_by_resource_type.setdefault(resource_type, [])
        config.derive_rules_by_resource_type[resource_type].append(f)

    return f


def tags(tags):
    def wrapped(f):
        for tag in tags:
            config.create_rule_by_tag[tag] = f

    return f
