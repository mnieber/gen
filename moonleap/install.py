from pathlib import Path

from moonleap.config import config
from moonleap.parser.term import word_to_term
from moonleap.prop import Prop


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
    extensions = []

    for f in [
        f
        for f in module.__dict__.values()
        if getattr(f, "__module__", "") == module.__name__
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

        if hasattr(f, "moonleap_extends_resource_type"):
            extensions.append(f)

    if hasattr(module, "meta"):
        if extensions:
            raise Exception(
                "Extensions should either be created in the module "
                + f"or in the meta function, not both.\nIn module: {module}"
            )
        extensions = module.meta()

    for c in extensions:
        resource_type = c.moonleap_extends_resource_type
        dest_class_meta = config.meta_by_resource_type.setdefault(resource_type, {})

        _install_output_dir(module, resource_type, c.__dict__, dest_class_meta)
        _install_templates(module, resource_type, c.__dict__, dest_class_meta)

        for base_type in c.__mro__:
            for prop_name, p in base_type.__dict__.items():
                if isinstance(p, Prop):
                    setattr(
                        resource_type, prop_name, property(p.get_value, p.set_value)
                    )
                    if p.add_value:
                        setattr(resource_type, "add_to_" + prop_name, p.add_value)
                    if p.doc_as_rel:
                        config.describe(resource_type, p.doc_as_rel)
