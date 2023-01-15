from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    def update_widget_spec(self):
        if "click:handler" in self.widget_spec.root.handler_terms:
            default_handler = "() => props.onClick && props.onClick()"
        else:
            default_handler = "() => console.log('Moonleap Todo')"

        onClick = self.widget_spec.values.get("onClick") or default_handler
        self.widget_spec.div.append_attrs([f"onClick={{ {onClick} }}"])
