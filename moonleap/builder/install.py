from moonleap.builder.config import config
from moonleap.parser.term import word_to_term
from moonleap.resource.memfield import MemField
from moonleap.resource.memfun import MemFun
from moonleap.resource.prop import DocMeta, Prop


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
        if not hasattr(resource_type, "doc_meta"):
            setattr(resource_type, "doc_meta", DocMeta())

        for base_type in c.__mro__:
            for prop_name, p in base_type.__dict__.items():
                if isinstance(p, Prop):
                    if p.update_doc_meta:
                        p.update_doc_meta(prop_name, resource_type.doc_meta)
                    setattr(
                        resource_type, prop_name, property(p.get_value, p.set_value)
                    )
                    if p.add_value:
                        setattr(resource_type, "add_to_" + prop_name, p.add_value)

                elif isinstance(p, MemFun):
                    setattr(resource_type, prop_name, p.f)

                elif isinstance(p, MemField):

                    def create_prop(name, default_value_factory):
                        private_name = "_" + name

                        def get_prop(self):
                            if not hasattr(self, private_name):
                                setattr(self, private_name, default_value_factory())

                            return getattr(self, private_name)

                        def set_prop(self, x):
                            setattr(self, private_name, x)

                        return property(get_prop, set_prop)

                    setattr(resource_type, prop_name, create_prop(prop_name, p.f))
