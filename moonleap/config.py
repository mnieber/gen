from importlib import import_module
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

    def get_output_dir(self, resource):
        output_dir = self.meta_by_resource_type.get(resource.__class__, {}).get(
            "output_dir", ""
        )
        return output_dir(resource) if callable(output_dir) else output_dir


config = Config()


def _install_templates(module, resource_type, src_class_meta, dest_class_meta):
    templates = src_class_meta.get("templates")
    if templates:
        dest_class_meta["templates"] = str(Path(module.__file__).parent / templates)


def _install_output_dir(module, resource_type, src_class_meta, dest_class_meta):
    dest_class_meta["output_dir"] = src_class_meta.get("output_dir")


def _resolve(resource_type):
    if isinstance(resource_type, str):
        p, type_name = resource_type.rsplit(".", 1)
        return getattr(import_module(p), type_name)
    return resource_type


def _install_parent_types(module, resource_type, src_class_meta, dest_class_meta):
    from moonleap.resource import create_prop_for_parents

    for prop_name, parent_resource_type in src_class_meta.get("parents", {}).items():
        parent_resource_type = _resolve(parent_resource_type)

        is_list = isinstance(parent_resource_type, list)
        parent_type = parent_resource_type[0] if is_list else parent_resource_type

        parent_types = dest_class_meta.setdefault("parent_types", [])
        if parent_type not in parent_types:
            parent_types.append(parent_type)

        setattr(resource_type, prop_name, create_prop_for_parents(parent_type, is_list))


def _install_child_types(module, resource_type, src_class_meta, dest_class_meta):
    from moonleap.resource import create_prop_for_children

    for prop_name, child_resource_type in src_class_meta.get("children", {}).items():
        child_resource_type = _resolve(child_resource_type)

        is_list = isinstance(child_resource_type, list)
        child_type = child_resource_type[0] if is_list else child_resource_type

        child_types = dest_class_meta.setdefault("child_types", [])
        if child_type not in child_types:
            child_types.append(child_type)

        setattr(resource_type, prop_name, create_prop_for_children(child_type, is_list))


def install(module):
    for f in [
        f
        for f in module.__dict__.values()
        if callable(f) and f.__module__ == module.__name__
    ]:
        if hasattr(f, "moonleap_create_rule_by_tag"):
            for tag, create_rule in f.moonleap_create_rule_by_tag.items():
                config.create_rule_by_tag[tag] = create_rule

        if hasattr(f, "moonleap_is_ittable_by_tag"):
            for tag, is_ittable in f.moonleap_is_ittable_by_tag.items():
                config.is_ittable_by_tag[tag] = is_ittable

        if hasattr(f, "moonleap_derive_resource"):
            resource_type = f.moonleap_derive_resource
            config.derive_rules_by_resource_type.setdefault(resource_type, [])
            config.derive_rules_by_resource_type[resource_type].append(f)

    for resource_type, src_class_meta in module.meta.items():
        dest_class_meta = config.meta_by_resource_type.setdefault(resource_type, {})
        _install_output_dir(module, resource_type, src_class_meta, dest_class_meta)
        _install_templates(module, resource_type, src_class_meta, dest_class_meta)
        _install_parent_types(module, resource_type, src_class_meta, dest_class_meta)
        _install_child_types(module, resource_type, src_class_meta, dest_class_meta)


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
