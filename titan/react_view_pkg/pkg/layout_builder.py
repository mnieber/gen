from titan.react_view_pkg.pkg.builder import Builder


class LayoutBuilder(Builder):
    def get_div(self, classes=None):
        places = []
        for child_widget_spec in self.widget_spec.child_widget_specs:
            if not child_widget_spec.place:
                raise Exception(
                    f"Child widget spec {child_widget_spec} does not have a place"
                )
            places.append(child_widget_spec.place)
        classes = self._get_classes(places)

        self._add_div_open(classes)
        self._add_child_widgets()
        return self._add_div_close()

    def _get_classes(self, places):
        places = sorted(places)
        if places == ["LeftSidebar", "RightMain"]:
            return ['"grid grid-cols-[400px,1fr]"']
        if places == ["BottomMain", "TopBar"]:
            return ['"grid grid-rows-[60px,1fr]"']
        if places == ["BottomPanel", "MiddlePanel", "TopPanel"]:
            return ['"grid grid-rows-3"']
        raise Exception(f"Unknown places: {places}")
