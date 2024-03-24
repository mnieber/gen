import moonleap.extension.props as P
from moonleap import create, extend, rule
from moonleap.spec.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module


@create("forms:module")
def create_forms_module(term):
    return create_react_module(ReactModule, term)


@rule("forms:module")
def created_forms_module(forms_module):
    forms_module.react_app.set_flags(
        ["utils/useScheduledCall", "utils/ValuePicker", "utils/slugify"]
    )


@extend(ReactApp)
class ExtendReactApp:
    forms_module = P.child(has, "forms:module")
