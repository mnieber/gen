from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, rule
from moonleap.verbs import has
from titan.react_pkg.packages.use_react_packages import use_react_packages
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("forms:module")
def create_module(term):
    module = ReactModule(name="forms")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("forms:module")
def forms_module_created(forms_module):
    use_react_packages(
        forms_module.react_app.get_module("utils"),
        ["useScheduledCall", "ValuePicker", "slugify"],
    )


@extend(ReactApp)
class ExtendReactApp:
    forms_module = P.child(has, "forms:module")
