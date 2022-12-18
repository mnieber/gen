from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, rule
from moonleap.verbs import has
from titan.react_pkg.packages.use_react_packages import use_react_packages
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("frames:module")
def create_module(term):
    module = ReactModule(name="frames")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@rule("frames:module")
def created_frames_module(frames_module):
    use_react_packages(
        frames_module.react_app.get_module("utils"),
        ["useScheduledCall", "ValuePicker", "slugify"],
    )


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module")
