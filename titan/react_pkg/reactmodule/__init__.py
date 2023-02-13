from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import MemFun, Prop, create, empty_rule, extend, kebab_to_camel, rule
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp

from . import props
from .resources import ReactModule  # noqa

rules = {
    ("react-app", has, "module"): empty_rule(),
}


base_tags = {"module": ["react-module"]}


def create_react_module(klass, term, template_dir):
    module = klass(name=kebab_to_camel(term.data))
    module.template_dir = template_dir
    module.template_context = dict(module=module)
    return module


@create("module")
def create_module(term):
    return create_react_module(ReactModule, term, Path(__file__).parent / "templates")


@rule("react-app", has, "module")
def react_app_has_module(react_app, module):
    react_app.renders(
        [module],
        f"src/{module.name}",
        module.template_context,
        [module.template_dir],
    )


@rule("react-app")
def assign_components_to_react_modules(react_app):
    from titan.react_pkg.component.props import create_forwards_for_widget_spec
    from titan.react_view_pkg.widgetregistry import get_widget_reg

    widget_reg = get_widget_reg()
    forwards = []
    for widget_spec in widget_reg.widget_specs():
        forwards += create_forwards_for_widget_spec(react_app, widget_spec)

    return forwards


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
