from importlib import import_module
from pathlib import Path

from moonleap.config import config


def _install_templates(module, resource_type, src_class_meta, dest_class_meta):
    templates = src_class_meta.get("templates")
    if templates:
        dest_class_meta["templates"] = str(Path(module.__file__).parent / templates)


def _install_output_dir(module, resource_type, src_class_meta, dest_class_meta):
    dest_class_meta["output_dir"] = src_class_meta.get("output_dir")


# Don't inline, it will create problems with the closure around parent_type
def create_prop_for_parents(parent_type, is_list):
    return (
        property(lambda self: self.parents_of_type(parent_type))
        if is_list
        else property(lambda self: self.parent_of_type(parent_type))
    )


# Don't inline, it will create problems with the closure around parent_type
def create_prop_for_children(child_type, is_list):
    return (
        property(lambda self: self.children_of_type(child_type))
        if is_list
        else property(lambda self: self.child_of_type(child_type))
    )


def _resolve(resource_type):
    is_list = isinstance(resource_type, list)
    t = resource_type[0] if is_list else resource_type
    if isinstance(resource_type, str):
        p, type_name = resource_type.rsplit(".", 1)
        t = getattr(import_module(p), type_name)
    return is_list, t


def _install_parent_types(module, resource_type, src_class_meta, dest_class_meta):
    for prop_name, parent_resource_type in src_class_meta.get("parents", {}).items():
        is_list, parent_type = _resolve(parent_resource_type)

        parent_types = dest_class_meta.setdefault("parent_types", [])
        if parent_type not in parent_types:
            parent_types.append(parent_type)

        setattr(resource_type, prop_name, create_prop_for_parents(parent_type, is_list))


def _install_child_types(module, resource_type, src_class_meta, dest_class_meta):
    for prop_name, child_resource_type in src_class_meta.get("children", {}).items():
        is_list, child_type = _resolve(child_resource_type)

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
