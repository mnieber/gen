from titan.widgets_pkg.pkg.load_widget_specs.widget_spec_parser import WidgetSpecParser


class BuilderPlaceMixin:
    def get_or_create_place_widget_spec(self, place, default_spec):
        place_widget_spec = self.widget_spec.find_child_with_place(place)
        if not place_widget_spec:
            place_widget_spec = WidgetSpecParser().parse(
                default_spec, parent_widget_spec=self.widget_spec
            )[0]
        return place_widget_spec
