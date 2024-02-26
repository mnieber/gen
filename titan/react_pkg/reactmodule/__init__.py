
import moonleap.packages.extensions.props as P
from moonleap import MemFun, Prop, create, empty_rule, extend, kebab_to_camel
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp

from . import props
from .resources import ReactModule  # noqa

base_tags = {"module": ["react-module"]}


def create_react_module(klass, term):
    module = klass(name=kebab_to_camel(term.data))
    return module


@create("module")
def create_module(term):
    return create_react_module(ReactModule, term)


@extend(ReactModule)
class ExtendModule:
    react_app = P.parent("react-app", has, required=True)
    module_path = Prop(props.module_path)


@extend(ReactApp)
class ExtendReactApp:
    modules = P.children(
        has, "module", lambda modules: sorted(modules, key=lambda x: x.name)
    )
    get_module = MemFun(props.get_module)


rules = {
    "react-app": {(has, "module"): empty_rule()},
}
