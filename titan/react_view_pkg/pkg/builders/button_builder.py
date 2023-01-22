from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    type = "Button"

    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["rowSkewer"])

        if "click:handler" in self.widget_spec.root.handler_terms:
            default_handler = "() => props.onClick && props.onClick()"
        else:
            default_handler = "() => console.log('Moonleap Todo')"

        onClick = self.get_value("onClick") or default_handler
        self.widget_spec.div.append_attrs([f"onClick={{ {onClick} }}"])
        self.widget_spec.div.elm = "button"

        t = self.get_value("size")
        if t == "big":
            self.widget_spec.div.append_styles(["bigButton"])

    def build(self):
        t = self.get_value("size")
        if t == "big":
            self.output.add(
                imports=["import { bigButton } from 'src/frames/components';"]
            )
