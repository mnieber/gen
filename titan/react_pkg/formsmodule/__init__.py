from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, rule
from moonleap.verbs import has
from titan.react_pkg.packages.use_react_package import use_react_package
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("forms:module")
def create_module(term):
    module = ReactModule(name="forms")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("forms:module")
def created_forms_module(forms_module):
    utils_module = forms_module.react_app.get_module("utils")
    use_react_package(utils_module, "hooks/useScheduledCall", "hooks")
    use_react_package(utils_module, "components/ValuePicker", "components")
    use_react_package(utils_module, "utils/slugify")


@extend(ReactApp)
class ExtendReactApp:
    forms_module = P.child(has, "forms:module")
