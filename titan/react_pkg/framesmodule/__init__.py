from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, extend
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule


@create("frames:module")
def create_module(term):
    module = ReactModule(name="frames")
    module.template_dir = Path(__file__).parent / "templates"
    return module


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module")
