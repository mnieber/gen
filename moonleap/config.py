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

    def has_children_of_type(self, resource_type, child_resource_type):
        class_meta = self.meta_by_resource_type.get(resource_type, {})
        return child_resource_type in class_meta.get("child_types", [])

    def has_parents_of_type(self, resource_type, parent_resource_type):
        class_meta = self.meta_by_resource_type.get(resource_type, {})
        return parent_resource_type in class_meta.get("parent_types", [])

    def get_templates(self, resource_type):
        return self.meta_by_resource_type.get(resource_type, {}).get("templates", [])


config = Config()


def _install_templates(module, resource_type, src_class_meta, dest_class_meta):
    templates = src_class_meta.get("templates")
    if templates:
        dest_class_meta["templates"] = str(Path(module.__file__).parent / templates)


def _install_parent_types(module, resource_type, src_class_meta, dest_class_meta):
    from moonleap.resource import create_prop_for_parents

    for prop_name, parent_resource_type in src_class_meta.get("parents", {}).items():
        is_list = isinstance(parent_resource_type, list)
        parent_type = parent_resource_type[0] if is_list else parent_resource_type

        parent_types = dest_class_meta.setdefault("parent_types", [])
        if parent_type not in parent_types:
            parent_types.append(parent_type)

        setattr(resource_type, prop_name, create_prop_for_parents(parent_type, is_list))


def _install_child_types(module, resource_type, src_class_meta, dest_class_meta):
    from moonleap.resource import create_prop_for_children

    for prop_name, child_resource_type in src_class_meta.get("children", {}).items():
        is_list = isinstance(child_resource_type, list)
        child_type = child_resource_type[0] if is_list else child_resource_type

        child_types = dest_class_meta.setdefault("child_types", [])
        if child_type not in child_types:
            child_types.append(child_type)

        setattr(resource_type, prop_name, create_prop_for_children(child_type, is_list))


def install(module):
    for resource_type, src_class_meta in module.meta.items():
        dest_class_meta = config.meta_by_resource_type.setdefault(resource_type, {})
        _install_templates(module, resource_type, src_class_meta, dest_class_meta)
        _install_parent_types(module, resource_type, src_class_meta, dest_class_meta)
        _install_child_types(module, resource_type, src_class_meta, dest_class_meta)


def derive(resource_type):
    def wrapped(f):
        config.derive_rules_by_resource_type.setdefault(resource_type, [])
        config.derive_rules_by_resource_type[resource_type].append(f)

    return wrapped


def tags(tags, is_ittable=False):
    def wrapped(f):
        for tag in tags:
            config.create_rule_by_tag[tag] = f
            config.is_ittable_by_tag[tag] = is_ittable

    return wrapped
