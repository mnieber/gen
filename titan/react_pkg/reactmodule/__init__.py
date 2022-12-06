from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.widgets_pkg.widgetregistry import get_widget_reg

from . import props
from .resources import ReactModule  # noqa

rules = {
    ("react-app", has, "module"): empty_rule(),
}


base_tags = {"module": ["react-module"]}


@create("module")
def create_module(term):
    module = ReactModule(name=kebab_to_camel(term.data))
    module.template_dir = Path(__file__).parent / "templates"
    module.template_context = dict(module=module)
    return module


@rule("react-app", has, "module")
def react_app_has_module(react_app, module):
    react_app.renders(
        [module],
        f"src/{module.name}",
        module.template_context,
        [module.template_dir],
    )


@rule("react-app")
def react_modules_provide_widgets(react_app):
    widget_reg = get_widget_reg()
    forwards = []
    for widget_spec in widget_reg.widget_specs():
        react_module_term_str = f"{widget_spec.module_name}:module"
        forwards += [
            create_forward(react_app, has, react_module_term_str),
            create_forward(react_module_term_str, has, widget_spec.widget_name),
        ]

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
