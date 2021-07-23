from moonleap.builder.config import config
from moonleap.parser.term import word_to_term
from moonleap.render.merge import add_file_merger, drop_file_merger
from moonleap.render.template_env import add_filter, drop_filter, get_filter
from moonleap.resource.memfield import MemField
from moonleap.resource.memfun import MemFun
from moonleap.resource.prop import Prop


# This class is a factory that creates uninstall functions.
class Uninstall:
    def __init__(self, uninstall_functions):
        self.uninstall_functions = uninstall_functions

    def key(self, obj, key):
        prev = obj.get(key, None)

        def uninstall():
            obj[key] = prev

        self.uninstall_functions.append(uninstall)

    def attr(self, obj, key):
        prev = getattr(obj, key, None)

        def uninstall():
            setattr(obj, key, prev)

        self.uninstall_functions.append(uninstall)

    def rule(self, config, rule):
        def uninstall():
            config.drop_rule(rule)

        self.uninstall_functions.append(uninstall)

    def file_merger(self, file_merger):
        def uninstall():
            drop_file_merger(file_merger)

        self.uninstall_functions.append(uninstall)

    def filter(self, name):
        prev = get_filter(name)

        def uninstall():
            if prev:
                add_filter(name, prev)
            else:
                drop_filter(name)

        self.uninstall_functions.append(uninstall)


def install_package(package, uninstall_functions):
    uninstall = Uninstall(uninstall_functions)

    for module in getattr(package, "modules", []):
        install_module(module, uninstall)

    for file_merger in getattr(package, "file_mergers", []):
        install_file_merger(file_merger, uninstall)

    for name, f in getattr(package, "filters", {}).items():
        install_filter(name, f, uninstall)


def install_filter(name, f, uninstall):
    uninstall.filter(name)
    add_filter(name, f)


def install_file_merger(file_merger, uninstall):
    uninstall.file_merger(file_merger)
    add_file_merger(file_merger)


def install_module(module, uninstall):
    extensions = []

    for f in [
        f
        for f in module.__dict__.values()
        if getattr(f, "__module__", "") == module.__name__
    ]:
        if hasattr(f, "moonleap_create_rule_by_tag"):
            for tag, create_rule in f.moonleap_create_rule_by_tag.items():
                term = word_to_term(tag, default_to_tag=True)
                uninstall.key(config.create_rule_by_term, term)
                config.create_rule_by_term[term] = create_rule

        if hasattr(f, "moonleap_rule"):
            rule = f.moonleap_rule
            uninstall.rule(config, rule)
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

    for extension in extensions:
        resource_type = extension.moonleap_extends_resource_type
        for base_type in extension.__mro__:
            for prop_name, p in base_type.__dict__.items():
                if isinstance(p, Prop):
                    uninstall.attr(resource_type, prop_name)
                    setattr(
                        resource_type, prop_name, property(p.get_value, p.set_value)
                    )
                    if p.add_value:
                        uninstall.attr(resource_type, "add_to_" + prop_name)
                        setattr(resource_type, "add_to_" + prop_name, p.add_value)

                elif isinstance(p, MemFun):
                    uninstall.attr(resource_type, prop_name)
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

                    uninstall.attr(resource_type, prop_name)
                    setattr(resource_type, prop_name, create_prop(prop_name, p.f))
