from moonleap import u0
from titan.react_view_pkg.pkg.builder import Builder


class IconBuilder(Builder):
    def build(self):
        name = u0(self.widget_spec.values["name"])
        self.output.set_flags([f"frames/{name}Icon"])
        self.add(
            lines=[f"<{name}Icon  />"],
            imports=[f"import {{ {name}Icon }} from 'src/frames/icons/{name}Icon';"],
        )
