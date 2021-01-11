from pathlib import Path

from moonleap.config import config
from moonleap.parser.term import word_to_term
from moonleap.props import Prop


def _install_templates(module, resource_type, src_class_meta, dest_class_meta):
    if "templates" in src_class_meta:
        templates = src_class_meta["templates"]

        def get_templates(resource):
            return str(
                Path(module.__file__).parent
                / (templates(resource) if callable(templates) else templates)
            )

        dest_class_meta["templates"] = get_templates


def _install_output_dir(module, resource_type, src_class_meta, dest_class_meta):
    if "output_dir" in src_class_meta:
        dest_class_meta["output_dir"] = src_class_meta["output_dir"]


def _install_props(module, resource_type, src_class_meta, dest_class_meta):
    for prop_name, (prop_get, prop_set) in src_class_meta.get("props", {}).items():
        setattr(resource_type, prop_name, property(prop_get, prop_set))


def install(module):
    for f in [
        f
        for f in module.__dict__.values()
        if callable(f) and f.__module__ == module.__name__
    ]:
        if hasattr(f, "moonleap_create_rule_by_tag"):
            for tag, create_rule in f.moonleap_create_rule_by_tag.items():
                term = word_to_term(tag, default_to_tag=True)
                config.create_rule_by_term[term] = create_rule

        if hasattr(f, "moonleap_derive_resource"):
            resource_type = f.moonleap_derive_resource
            config.derive_rules_by_resource_type.setdefault(resource_type, [])
            config.derive_rules_by_resource_type[resource_type].append(f)

        if hasattr(f, "moonleap_rule"):
            config.add_rule(f.moonleap_rule)

    for c in module.meta():
        resource_type = c._extends_resource_type
        dest_class_meta = config.meta_by_resource_type.setdefault(resource_type, {})

        _install_output_dir(module, resource_type, c.__dict__, dest_class_meta)
        _install_templates(module, resource_type, c.__dict__, dest_class_meta)

        for prop_name, p in c.__dict__.items():
            if isinstance(p, Prop):
                setattr(resource_type, prop_name, property(p.get, p.set))
                if p.add:
                    setattr(resource_type, "add_to_" + prop_name, p.add)
