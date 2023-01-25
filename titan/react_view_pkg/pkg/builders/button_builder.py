from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    type = "Button"

    @property
    def size(self):
        return self.get_value("size") or "medium"

    def update_widget_spec(self):
        self.widget_spec.div.prepend_styles(["rowSkewer"])

        if "click:handler" in self.widget_spec.root.handler_terms:
            default_handler = "() => props.onClick && props.onClick()"
        else:
            default_handler = "() => console.log('Moonleap Todo')"

        onClick = self.get_value("onClick") or default_handler
        self.widget_spec.div.append_attrs([f"onClick={{ {onClick} }}"])
        self.widget_spec.div.elm = "button"

        if self.size == "big":
            self.widget_spec.div.append_styles(["bigButton"])

        elif self.size == "medium":
            self.widget_spec.div.append_styles(["button"])

    def build(self):
        self.output.add(imports=["import { rowSkewer } from 'src/frames/components';"])

        if self.size == "big":
            self.output.add(
                imports=["import { bigButton } from 'src/frames/components';"]
            )

        elif self.size == "medium":
            self.output.add(imports=["import { button } from 'src/frames/components';"])
