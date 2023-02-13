from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, extend
from moonleap.blocks.verbs import has
from titan.react_pkg.reactapp import ReactApp
from titan.react_pkg.reactmodule import ReactModule, create_react_module


@create("frames:module")
def create_frames_module(term):
    return create_react_module(ReactModule, term, Path(__file__).parent / "templates")


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module")
