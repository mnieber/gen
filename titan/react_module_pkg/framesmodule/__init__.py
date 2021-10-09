from pathlib import Path

import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.react_pkg.reactapp import ReactApp


@rule("react-app", has, "frames:module")
def react_app_has_frames_module(react_app, frames_module):
    frames_module.add_template_dir(Path(__file__).parent / "templates")
    frames_module.add_template_dir(
        Path(__file__).parent / "templates_css_utils",
        skip_render=lambda x: x.react_app.has_tailwind_css,
    )


@extend(ReactApp)
class ExtendReactApp:
    frames_module = P.child(has, "frames:module", required=True)
