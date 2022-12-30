from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, extend, rule
from moonleap.blocks.verbs import has
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("forms:module")
def create_module(term):
    module = ReactModule(name="forms")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("forms:module")
def created_forms_module(forms_module):
    get_root_resource().set_flags(
        ["utils/useScheduledCall", "utils/ValuePicker", "utils/slugify"]
    )


@extend(ReactApp)
class ExtendReactApp:
    forms_module = P.child(has, "forms:module")
