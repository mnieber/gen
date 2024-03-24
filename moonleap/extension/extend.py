from moonleap.extension.memfield import MemField
from moonleap.extension.memfun import MemFun
from moonleap.extension.prop import Prop


def apply_extension(resource_type, extension):
    for base_type in reversed(extension.__mro__):
        for prop_name, p in base_type.__dict__.items():
            if isinstance(p, Prop):
                setattr(resource_type, prop_name, property(p.get_value, p.set_value))

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


def extend(resource_type):
    def wrapped(props):
        setattr(props, "moonleap_extends_resource_type", resource_type)
        return props

    return wrapped
