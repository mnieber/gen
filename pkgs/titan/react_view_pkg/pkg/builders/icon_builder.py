from titan.react_view_pkg.pkg.builder import Builder

from moonleap import u0
from moonleap.render.render_mixin import get_root_resource


class IconBuilder(Builder):
    def build(self):
        name = u0(self.widget_spec.values["name"])
        self.output.set_flags([f"frames/{name}Icon"])

        if name in ("New",):
            get_root_resource().set_flags(["app/UIkitIcons"])

        self.add(
            lines=[f"<{name}Icon  />"],
            imports=[f"import {{ {name}Icon }} from 'src/frames/icons/{name}Icon';"],
        )
