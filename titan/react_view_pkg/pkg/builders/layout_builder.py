from titan.react_view_pkg.pkg.builder import Builder
from titan.widgetspec.widget_spec import WidgetSpec


class LayoutBuilder(Builder):
    type = "Layout"

    def build(self):
        places, more_classes = _get_places_and_classes_from_widget_specs(
            self.widget_spec.child_widget_specs
        )

        self.widget_spec.div.prepend_styles(more_classes)
        self._add_div_open()
        self._add_child_widgets(
            _filtered_child_widget_specs(places, self.widget_spec.child_widget_specs)
        )
        self._add_div_close()


def _filtered_child_widget_specs(places, child_widget_specs):
    result = []
    for place in places:
        found = False
        for child_widget_spec in child_widget_specs:
            if child_widget_spec.place == place:
                result.append(child_widget_spec)
                found = True
                break
        if not found:
            result.append(WidgetSpec(widget_base_types=["Empty"]))
    return result


def _get_ordered_places(places, ordered_places):
    if set(places) == set(ordered_places):
        return ordered_places
    return None


def _get_places_and_classes_from_widget_specs(widget_specs):
    places = []
    for child_widget_spec in widget_specs:
        if not child_widget_spec.place:
            raise Exception(f"Layout does not have a place for {child_widget_spec}")
        places.append(child_widget_spec.place)

    if ordered_places := _get_ordered_places(places, ["LeftSidebar", "RightMain"]):
        return ordered_places, ['"grid grid-cols-[400px,1fr]"']
    if ordered_places := _get_ordered_places(places, ["LeftMain", "RightSidebar"]):
        return ordered_places, ['"grid grid-cols-[1fr,400px]"']
    if ordered_places := _get_ordered_places(places, ["TopBar", "BottomMain"]):
        return ordered_places, ['"grid grid-rows-[60px,1fr]"']
    if ordered_places := _get_ordered_places(
        places, ["BottomPanel", "MiddlePanel", "TopPanel"]
    ):
        return ordered_places, ['"grid grid-rows-3"']
    raise Exception(f"Unknown places: {places}")
