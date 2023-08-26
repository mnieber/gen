from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, extend, rule
from moonleap.blocks.verbs import has
from moonleap.render.render_mixin import get_root_resource
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module


@create("forms:module")
def create_forms_module(term):
    return create_react_module(ReactModule, term, Path(__file__).parent / "templates")


@rule("forms:module")
def created_forms_module(forms_module):
    forms_module.react_app.set_flags(
        ["utils/useScheduledCall", "utils/ValuePicker", "utils/slugify"]
    )


@extend(ReactApp)
class ExtendReactApp:
    forms_module = P.child(has, "forms:module")
