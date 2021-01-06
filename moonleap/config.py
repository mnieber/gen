from pathlib import Path


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

    def get_output_dir(self, resource):
        output_dir = self.meta_by_resource_type.get(resource.__class__, {}).get(
            "output_dir", ""
        )
        return output_dir(resource) if callable(output_dir) else output_dir


config = Config()


def derive(resource_type):
    def wrapped(f):
        f.moonleap_derive_resource = resource_type

    return wrapped


def tags(tags, is_ittable=False):
    def wrapped(f):
        f.moonleap_create_rule_by_tag = {}
        for tag in tags:
            f.moonleap_create_rule_by_tag[tag] = f

        f.moonleap_is_ittable_by_tag = {}
        for tag in tags:
            f.moonleap_is_ittable_by_tag[tag] = is_ittable

        return f

    return wrapped


def output_dir_from(prop_name):
    def get_output_dir(resource):
        if hasattr(resource, prop_name):
            prop = getattr(resource, prop_name)
            return config.get_output_dir(prop)
        return ""

    return get_output_dir


def output_path_from(prop_name):
    return lambda x: Path(output_dir_from(prop_name)(x))
