from titan.react_view_pkg.pkg.builder import Builder


class ButtonBuilder(Builder):
    def update_widget_spec(self):
        onClick = (
            self.widget_spec.values.get("onClick")
            or '() => console.log("Moonleap Todo")'
        )
        self.widget_spec.div.append_attrs([f"onClick={{ {onClick} }}"])
