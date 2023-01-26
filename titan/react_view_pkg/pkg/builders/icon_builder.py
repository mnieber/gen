from moonleap.render.render_mixin import get_root_resource
from titan.react_view_pkg.pkg.builder import Builder


class IconBuilder(Builder):
    type = "Icon"

    def build(self):
        name = self.get_value("name")
        self.output.set_flags([f"frames/{name}Icon"])

        if name in ("plus",):
            get_root_resource().set_flags(["app/UIkitIcons"])

        self.output.add(
            lines=[f'<Icon name="{name}" />'],
            imports=[f"import {{ Icon }} from 'src/frames/components';"],
        )
