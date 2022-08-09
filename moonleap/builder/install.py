from moonleap.render.file_merger import add_file_merger
from moonleap.render.template_env import add_filter
from moonleap.render.transforms import register_transforms
from moonleap.resource.memfield import MemField
from moonleap.resource.memfun import MemFun
from moonleap.resource.prop import Prop


def get_symbols(module):
    return [
        f
        for f in module.__dict__.values()
        if getattr(f, "__module__", "") == module.__name__
    ]


def install_package(package):
    for module in getattr(package, "modules", []):
        install_module(module)


def install_module(module):
    extensions = []

    for f in get_symbols(module):
        if hasattr(f, "moonleap_extends_resource_type"):
            extensions.append(f)

    if hasattr(module, "meta"):
        if extensions:
            raise Exception(
                "Extensions should either be created in the module "
                + f"or in the meta function, not both.\nIn module: {module}"
            )
        extensions = module.meta()

    register_transforms(
        getattr(module, "transforms", []),
        getattr(module, "post_transforms", []),
    )

    for file_merger in getattr(module, "file_mergers", []):
        add_file_merger(file_merger)

    for name, f in getattr(module, "filters", {}).items():
        add_filter(name, f)

    for extension in extensions:
        resource_type = extension.moonleap_extends_resource_type
        for base_type in reversed(extension.__mro__):
            for prop_name, p in base_type.__dict__.items():
                if isinstance(p, Prop):
                    setattr(
                        resource_type, prop_name, property(p.get_value, p.set_value)
                    )

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
