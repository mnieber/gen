from pathlib import Path


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.derive_rules_by_resource_type = {}
        self.is_ittable_by_tag = {}
        self.meta_by_resource_type = {}

    def get_derive_rules(self, resource_type):
        return self.derive_rules_by_resource_type.get(resource_type) or {}

    def get_meta(self, resource_type):
        return self.meta_by_resource_type.get(resource_type, {})

    def get_child_types(self, resource_type):
        return self.get_meta(resource_type).get("child_types", [])

    def get_parent_types(self, resource_type):
        return self.get_meta(resource_type).get("parent_types", [])

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
        return f

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
        __import__("pudb").set_trace()
        if hasattr(resource, prop_name):
            prop = getattr(resource, prop_name)
            return config.get_output_dir(prop)
        return ""

    return get_output_dir


def output_path_from(prop_name):
    return lambda x: Path(output_dir_from(prop_name)(x))
