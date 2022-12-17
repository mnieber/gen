from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    def update_widget_spec(self):
        def add_click_handler():
            if "click:handler" in self.widget_spec.root.named_props:
                default_handler = "() => props.onClick()"
            else:
                default_handler = "() => console.log('Moonleap Todo')"

            onClick = self.widget_spec.values.get("onClick") or default_handler
            self.widget_spec.div.append_attrs([f"onClick={{ {onClick} }}"])

        return add_click_handler
